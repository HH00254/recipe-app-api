"""
Views for the recipe APIs.

A View is the layer responsible for handling HTTP requests.

Request flow:

Client (React/Postman/Mobile)
        |
        v
urls.py / router
        |
        v
RecipeViewSet  <---- We are here
        |
        v
Serializer
        |
        v
Model / Database
        |
        v
JSON Response

"""


# Import DRF ViewSets.
#
# ViewSets combine multiple API operations into one class.
#
# Instead of manually writing:
#
#   get()
#   post()
#   put()
#   patch()
#   delete()
#
# ModelViewSet provides them automatically.
#
from rest_framework import viewsets


# TokenAuthentication allows DRF to identify
# which user is making the request.
#
# Example:
#
# Header:
#
# Authorization: Token abc123xyz
#
# DRF checks that token and attaches the user:
#
# request.user = authenticated_user
#
from rest_framework.authentication import TokenAuthentication


# Permission classes decide who is allowed
# to access this API.
#
# IsAuthenticated means:
#
# Logged in user  -> allowed
# Anonymous user -> rejected (401)
#
from rest_framework.permissions import IsAuthenticated


# Import the database model.
#
# Recipe represents the table in PostgreSQL.
#
# Example:
#
# Recipe.objects.all()
#
# roughly becomes:
#
# SELECT * FROM recipe;
#
from core.models import Recipe


# Import serializer classes.
#
# Serializers convert between:
#
# Python/Django objects
#          |
#          v
#        JSON
#
from recipe import serializers



class RecipeViewSet(viewsets.ModelViewSet):
    """
    View for managing recipe APIs.

    ModelViewSet automatically creates:

    GET     /recipes/
        -> list all recipes

    POST    /recipes/
        -> create recipe

    GET     /recipes/{id}/
        -> retrieve one recipe

    PUT     /recipes/{id}/
        -> replace recipe

    PATCH   /recipes/{id}/
        -> update part of recipe

    DELETE  /recipes/{id}/
        -> delete recipe


    Behind the scenes DRF provides:

    list()
    create()
    retrieve()
    update()
    partial_update()
    destroy()

    """

    
    # Tell the ViewSet which serializer controls
    # converting Recipe objects into JSON.
    #
    # Example:
    #
    # Recipe object:
    #
    # Recipe(
    #    title="Pizza",
    #    time_minutes=20
    # )
    #
    # becomes:
    #
    # {
    #   "title": "Pizza",
    #   "time_minutes":20
    # }
    #
    serializer_class = serializers.RecipeDetailSerializer



    # Base database query.
    #
    # This creates the starting queryset.
    #
    # It does NOT immediately hit the database.
    #
    # Django QuerySets are lazy.
    #
    # Think:
    #
    # "Prepare this SQL query"
    #
    # not:
    #
    # "Run this SQL query"
    queryset = Recipe.objects.all()



    # Authentication method.
    #
    # When a request arrives:
    #
    # 1. DRF reads Authorization header
    #
    # 2. Looks for token
    #
    # 3. Finds matching user
    #
    # 4. Sets:
    #
    # self.request.user
    #
    authentication_classes = [
        TokenAuthentication
    ]



    # Security rule.
    #
    # User must be logged in.
    #
    # Without this:
    #
    # Anyone could call:
    #
    # GET /recipes/
    #
    permission_classes = [
        IsAuthenticated
    ]



    def get_queryset(self):
        """
        Return objects belonging only to the
        current authenticated user.


        Why override this?

        Default ModelViewSet would do:

            Recipe.objects.all()


        Meaning:

            User A sees User B recipes ❌


        We want:

            Recipe.objects.filter(
                user=current_user
            )


        Example:

        Database:

        id | recipe | user
        ------------------
        1  | Pizza  | Bob
        2  | Pasta  | Sue


        If Bob logs in:

        request.user = Bob


        Query becomes:

        SELECT *
        FROM recipe
        WHERE user = Bob;


        Result:

        Bob only sees Pizza

        """


        return (
            self.queryset

            # Filter recipes where the user column
            # matches whoever owns the token.
            #
            .filter(
                user=self.request.user
            )


            # Newest recipes first.
            #
            # -id means descending order:
            #
            # 10
            # 9
            # 8
            #
            .order_by('-id')
        )



    def perform_create(self, serializer):
        """
        Create a new recipe.

        This method runs when:

        POST /recipes/


        Normal ModelViewSet does:

            serializer.save()


        But our Recipe model requires:

            user_id


        We don't want users sending:

        {
            "user": 5
        }


        because they could create recipes
        for someone else.


        Instead:

        We get the user securely from:

            request.user


        Then inject it during save.

        """

        serializer.save(
            user=self.request.user
        )

    def get_serializer_class(self):
        """
        Return appropriate serializer class.

        This method runs when:

        GET /recipes/
        GET /recipes/{id}/


        We want:

        GET /recipes/       -> RecipeSerializer
        GET /recipes/{id}/ -> RecipeDetailSerializer

        """


        if self.action == 'list':
            return serializers.RecipeSerializer

        return self.serializer_class
    
    