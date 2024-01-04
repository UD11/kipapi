import graphene
from graphene_django.types import DjangoObjectType
from django.contrib.auth.models import User
from .models import UserProfile
from graphene import String, Mutation
import graphql_jwt
from graphql_jwt.decorators import login_required
from django.contrib.auth import authenticate, logout
from .leetcode_scraper import get_leetcode_stats
from .gfg_scraper import get_geeksforgeeks_stats
from .codechef_scraper import get_codechef_stats
from .codeforces_scraper import get_codeforces_stats
class GeeksforGeeksStatsType(graphene.ObjectType):
    geeksforgeeks_username = graphene.String()
    total_problems_solved = graphene.Int()
    easy_solved = graphene.Int()
    medium_solved = graphene.Int()
    hard_solved = graphene.Int()
    overall_coding_score = graphene.Float()
class LeetCodeStatsType(graphene.ObjectType):
    leetcode_username = graphene.String()
    candidate_name = graphene.String()
    questions_done = graphene.Int()
    easy_solved = graphene.Int()
    medium_solved = graphene.Int()
    hard_solved = graphene.Int()
    contest_rating = graphene.String()
    total_active_days = graphene.Int()

class CodeChefType(graphene.ObjectType):
    codechef_username = graphene.String()
    rating = graphene.String()
    stars = graphene.String()
    # highest_rating = graphene.String()
    practice_problems_solved = graphene.Int()
    contests_participated = graphene.Int()
    division = graphene.String()

class CodeforcesStatsType(graphene.ObjectType):
    # codeforces_handle = graphene.String()
    rating = graphene.String()
    solved_problems = graphene.Int()
    rank = graphene.String()


class UserProfileType(DjangoObjectType):
    class Meta:
        model = UserProfile

class UserType(DjangoObjectType):
    class Meta:
        model = User



class Query(graphene.ObjectType):
    user_profile = graphene.Field(UserProfileType, id=graphene.Int(required=True))
    leetcode_stats = graphene.Field(
        LeetCodeStatsType,
        username=graphene.String(required=True),
    )
    geeksforgeeks_stats = graphene.Field(
        GeeksforGeeksStatsType,
        username=graphene.String(required=True),
    )
    codechef_info = graphene.Field(CodeChefType, username=graphene.String(required=True))

    codeforces_stats = graphene.Field(
        CodeforcesStatsType,
        username=graphene.String(required=True)
    )

    # @login_required
    def resolve_user_profile(self, info, id):
        return UserProfile.objects.get(user__id=id)

    def resolve_leetcode_stats(self, info, username):
        leetcode_stats_data = get_leetcode_stats(username)
        return LeetCodeStatsType(**leetcode_stats_data)

    def resolve_geeksforgeeks_stats(self, info, username):
        geeksforgeeks_stats_data = get_geeksforgeeks_stats(username)
        return GeeksforGeeksStatsType(**geeksforgeeks_stats_data)

    def resolve_codechef_info(self, info, username):
        codechef_info = get_codechef_stats(username)
        return CodeChefType(**codechef_info)

    def resolve_codeforces_stats(self, info, username):
        codeforces_stats = get_codeforces_stats(username)
        return CodeforcesStatsType(**codeforces_stats) if codeforces_stats else None


class SignUpMutation(Mutation):
    class Arguments:
        username = String(required=True)
        password = String(required=True)
        email = String(required=True)
        first_name = String(required=True)
        last_name = String(required=True)
        enrollment_number = String(required=True)
        passout_year = String(required=True)
        state = String(required=True)
        department = String(required=True)

    success = graphene.Boolean()

    def mutate(self, info, username, password, email, first_name, last_name, enrollment_number, passout_year,
               department, state):
        if User.objects.filter(username=username).exists() or User.objects.filter(
                email=email).exists() or UserProfile.objects.filter(enrollment_number=enrollment_number).exists():
            return SignUpMutation(success=False)

        user = User.objects.create_user(
            username=username,
            password=password,
            email=email,
            first_name=first_name,
            last_name=last_name,
        )

        UserProfile.objects.create(
            user=user,
            passout_year=passout_year,
            department=department,
            state=state,
            enrollment_number=enrollment_number,
        )

        return SignUpMutation(success=True)

class SignInMutation(Mutation):
    class Arguments:
        password=String(required=True)
        username = String(required=True)

    success = graphene.Boolean()
    token = graphene.String()

    def mutate(self,info,username,password):
        user = authenticate(username=username,password=password)
        if not user:
            return SignInMutation(success=False)
        if user:
            token = graphql_jwt.shortcuts.get_token(user)
            return SignInMutation(success=True,token=token)


class SignOutMutation(Mutation):
    success = graphene.Boolean()

    @login_required
    def mutate(self,info):
        user = info.context.user
        logout(info.context)
        return SignOutMutation(success=True)



class Mutation(graphene.ObjectType):
    obtain_jwt_token = graphql_jwt.ObtainJSONWebToken.Field()
    refresh_jwt_token = graphql_jwt.Refresh.Field()
    verify_jwt_token = graphql_jwt.Verify.Field()
    signup = SignUpMutation.Field()
    signin = SignInMutation.Field()
    signout = SignOutMutation.Field()

schema = graphene.Schema(query=Query, mutation=Mutation, types=[UserProfileType, UserType])
