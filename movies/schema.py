import graphene
from graphene_django.types import DjangoObjectType, ObjectType
from .models import Actor, Movie


class ActorType(DjangoObjectType):
    class Meta:
        model = Actor


class MovieType(DjangoObjectType):
    class Meta:
        model = Movie


class Query(ObjectType):
    actor = graphene.Field(ActorType, id=graphene.Int())
    movie = graphene.Field(MovieType, id=graphene.Int())
    actors = graphene.List(ActorType)
    movies = graphene.List(MovieType)

    def resolve_actor(self, info, **kwargs):
        id = kwargs.get('id')

        if id is not None:
            return Actor.objects.get(pk=id)

        return None

    def resolve_movie(self, info, **kwargs):
        id = kwargs.get('id')

        if id is not None:
            return Movie.objects.get(pk=id)

    def resolve_actors(self, info, **kwargs):
        return Actor.objects.all()

    def resolve_movies(self, info, **kwargs):
        return Movie.objects.all()


class ActorInput(graphene.InputObjectType):
    id = graphene.ID()
    name = graphene.String()


class MovieInput(graphene.InputObjectType):
    id = graphene.ID()
    title = graphene.String()
    actors = graphene.List(ActorInput)
    year = graphene.Int()


class CreateActor(graphene.Mutation):
    class Arguments:
        input = ActorInput(required=True)

    actor = graphene.Field(ActorType)

    @staticmethod
    def mutate(root, info, input=None):
        actor_instance = Actor(name=input.name)
        actor_instance.save()
        return CreateActor(actor=actor_instance)


class UpdateActor(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        input = ActorInput(required=True)

    actor = graphene.Field(ActorType)

    @staticmethod
    def mutate(root, info, id, input=None):
        actor_instance = Actor.objects.get(pk=id)

        if actor_instance:
            actor_instance.name = input.name
            actor_instance.save()
            return UpdateActor(actor=actor_instance)

        return UpdateActor(actor=None)


class CreateMovie(graphene.Mutation):
    class Arguments:
        input = MovieInput(required=True)

    movie = graphene.Field(MovieType)

    @staticmethod
    def mutate(root, info, input=None):
        actors = []
        for actor_input in input.actors:
            actor = Actor.objects.get(pk=actor_input.id)

            if actor is None:
                return CreateMovie(movie=None)

            actors.append(actor)

        movie_instance = Movie(
            title=input.title,
            year=input.year
        )

        movie_instance.save()
        movie_instance.actors.set(actors)

        return CreateMovie(movie=movie_instance)


class UpdateMovie(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        input = MovieInput(required=True)

    movie = graphene.Field(MovieType)

    @staticmethod
    def mutate(root, info, id, input=None):
        movie_instance = Movie.objects.get(pk=id)
        if movie_instance:
            actors = []
            for actor_input in input.actors:
                actor = Actor.objects.get(pk=actor_input.id)
                if actor is None:
                    return UpdateMovie(movie=None)
                actors.append(actor)

            movie_instance.title = input.title
            movie_instance.year = input.year
            movie_instance.save()
            movie_instance.actors.set(actors)
            return UpdateMovie(movie=movie_instance)
        return UpdateMovie(movie=None)


class Mutation(graphene.ObjectType):
    create_actor = CreateActor.Field()
    update_actor = UpdateActor.Field()
    create_movie = CreateMovie.Field()
    update_movie = UpdateMovie.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
