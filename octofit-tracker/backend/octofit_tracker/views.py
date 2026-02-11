from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum
from .models import User, Team, Activity, Leaderboard, Workout
from .serializers import (
    UserSerializer,
    TeamSerializer,
    ActivitySerializer,
    LeaderboardSerializer,
    WorkoutSerializer
)


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-created_at')
    serializer_class = UserSerializer
    
    @action(detail=False, methods=['get'])
    def by_team(self, request):
        """Get users by team"""
        team = request.query_params.get('team', None)
        if team:
            users = User.objects.filter(team=team)
            serializer = self.get_serializer(users, many=True)
            return Response(serializer.data)
        return Response({'error': 'Team parameter required'}, status=status.HTTP_400_BAD_REQUEST)


class TeamViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows teams to be viewed or edited.
    """
    queryset = Team.objects.all().order_by('-total_points')
    serializer_class = TeamSerializer
    
    @action(detail=True, methods=['get'])
    def members(self, request, pk=None):
        """Get all members of a team"""
        team = self.get_object()
        users = User.objects.filter(team=team.name)
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def standings(self, request):
        """Get team standings"""
        teams = Team.objects.all().order_by('-total_points')
        serializer = self.get_serializer(teams, many=True)
        return Response(serializer.data)


class ActivityViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows activities to be viewed or edited.
    """
    queryset = Activity.objects.all().order_by('-date')
    serializer_class = ActivitySerializer
    
    @action(detail=False, methods=['get'])
    def by_user(self, request):
        """Get activities for a specific user"""
        user_email = request.query_params.get('user_email', None)
        if user_email:
            activities = Activity.objects.filter(user_email=user_email).order_by('-date')
            serializer = self.get_serializer(activities, many=True)
            return Response(serializer.data)
        return Response({'error': 'user_email parameter required'}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def recent(self, request):
        """Get recent activities (limit 20)"""
        activities = Activity.objects.all().order_by('-date')[:20]
        serializer = self.get_serializer(activities, many=True)
        return Response(serializer.data)


class LeaderboardViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows leaderboard to be viewed or edited.
    """
    queryset = Leaderboard.objects.all().order_by('rank')
    serializer_class = LeaderboardSerializer
    
    @action(detail=False, methods=['get'])
    def top(self, request):
        """Get top 10 users"""
        top_users = Leaderboard.objects.all().order_by('rank')[:10]
        serializer = self.get_serializer(top_users, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_team(self, request):
        """Get leaderboard filtered by team"""
        team = request.query_params.get('team', None)
        if team:
            users = Leaderboard.objects.filter(team=team).order_by('rank')
            serializer = self.get_serializer(users, many=True)
            return Response(serializer.data)
        return Response({'error': 'team parameter required'}, status=status.HTTP_400_BAD_REQUEST)


class WorkoutViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows workouts to be viewed or edited.
    """
    queryset = Workout.objects.all().order_by('name')
    serializer_class = WorkoutSerializer
    
    @action(detail=False, methods=['get'])
    def by_type(self, request):
        """Get workouts by type"""
        workout_type = request.query_params.get('type', None)
        if workout_type:
            workouts = Workout.objects.filter(type=workout_type)
            serializer = self.get_serializer(workouts, many=True)
            return Response(serializer.data)
        return Response({'error': 'type parameter required'}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def by_difficulty(self, request):
        """Get workouts by difficulty"""
        difficulty = request.query_params.get('difficulty', None)
        if difficulty:
            workouts = Workout.objects.filter(difficulty=difficulty)
            serializer = self.get_serializer(workouts, many=True)
            return Response(serializer.data)
        return Response({'error': 'difficulty parameter required'}, status=status.HTTP_400_BAD_REQUEST)
