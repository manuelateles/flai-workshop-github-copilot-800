from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APITestCase
from rest_framework import status
from .models import User, Team, Activity, Leaderboard, Workout


class UserModelTest(TestCase):
    """Test cases for User model"""
    
    def setUp(self):
        self.user = User.objects.create(
            name='Test Hero',
            email='hero@test.com',
            team='Test Team'
        )
    
    def test_user_creation(self):
        """Test that a user can be created"""
        self.assertEqual(self.user.name, 'Test Hero')
        self.assertEqual(self.user.email, 'hero@test.com')
        self.assertEqual(self.user.team, 'Test Team')
    
    def test_user_str(self):
        """Test the string representation of user"""
        self.assertEqual(str(self.user), 'Test Hero')


class TeamModelTest(TestCase):
    """Test cases for Team model"""
    
    def setUp(self):
        self.team = Team.objects.create(
            name='Test Team',
            description='A test team',
            members_count=5,
            total_points=100
        )
    
    def test_team_creation(self):
        """Test that a team can be created"""
        self.assertEqual(self.team.name, 'Test Team')
        self.assertEqual(self.team.members_count, 5)
        self.assertEqual(self.team.total_points, 100)
    
    def test_team_str(self):
        """Test the string representation of team"""
        self.assertEqual(str(self.team), 'Test Team')


class ActivityModelTest(TestCase):
    """Test cases for Activity model"""
    
    def setUp(self):
        self.activity = Activity.objects.create(
            user_email='hero@test.com',
            activity_type='Running',
            duration=30,
            calories_burned=300,
            points=30,
            date=timezone.now()
        )
    
    def test_activity_creation(self):
        """Test that an activity can be created"""
        self.assertEqual(self.activity.user_email, 'hero@test.com')
        self.assertEqual(self.activity.activity_type, 'Running')
        self.assertEqual(self.activity.duration, 30)
    
    def test_activity_str(self):
        """Test the string representation of activity"""
        self.assertEqual(str(self.activity), 'hero@test.com - Running')


class WorkoutModelTest(TestCase):
    """Test cases for Workout model"""
    
    def setUp(self):
        self.workout = Workout.objects.create(
            name='Test Workout',
            description='A test workout',
            type='Cardio',
            difficulty='Medium',
            duration=45,
            calories_per_session=400,
            points_per_session=40
        )
    
    def test_workout_creation(self):
        """Test that a workout can be created"""
        self.assertEqual(self.workout.name, 'Test Workout')
        self.assertEqual(self.workout.type, 'Cardio')
        self.assertEqual(self.workout.difficulty, 'Medium')
    
    def test_workout_str(self):
        """Test the string representation of workout"""
        self.assertEqual(str(self.workout), 'Test Workout')


class UserAPITest(APITestCase):
    """Test cases for User API endpoints"""
    
    def setUp(self):
        self.user = User.objects.create(
            name='API Test Hero',
            email='apitest@hero.com',
            team='Test Team'
        )
    
    def test_get_users(self):
        """Test retrieving list of users"""
        response = self.client.get('/api/users/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_create_user(self):
        """Test creating a new user"""
        data = {
            'name': 'New Hero',
            'email': 'newhero@test.com',
            'team': 'New Team'
        }
        response = self.client.post('/api/users/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class TeamAPITest(APITestCase):
    """Test cases for Team API endpoints"""
    
    def setUp(self):
        self.team = Team.objects.create(
            name='API Test Team',
            description='Test team for API',
            members_count=3,
            total_points=150
        )
    
    def test_get_teams(self):
        """Test retrieving list of teams"""
        response = self.client.get('/api/teams/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_team_standings(self):
        """Test retrieving team standings"""
        response = self.client.get('/api/teams/standings/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ActivityAPITest(APITestCase):
    """Test cases for Activity API endpoints"""
    
    def setUp(self):
        self.activity = Activity.objects.create(
            user_email='test@hero.com',
            activity_type='Swimming',
            duration=60,
            calories_burned=500,
            points=50,
            date=timezone.now()
        )
    
    def test_get_activities(self):
        """Test retrieving list of activities"""
        response = self.client.get('/api/activities/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_recent_activities(self):
        """Test retrieving recent activities"""
        response = self.client.get('/api/activities/recent/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class WorkoutAPITest(APITestCase):
    """Test cases for Workout API endpoints"""
    
    def setUp(self):
        self.workout = Workout.objects.create(
            name='API Test Workout',
            description='Workout for API testing',
            type='Strength',
            difficulty='Hard',
            duration=45,
            calories_per_session=450,
            points_per_session=45
        )
    
    def test_get_workouts(self):
        """Test retrieving list of workouts"""
        response = self.client.get('/api/workouts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_create_workout(self):
        """Test creating a new workout"""
        data = {
            'name': 'New Workout',
            'description': 'A brand new workout',
            'type': 'Cardio',
            'difficulty': 'Easy',
            'duration': 30,
            'calories_per_session': 300,
            'points_per_session': 30
        }
        response = self.client.post('/api/workouts/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class LeaderboardAPITest(APITestCase):
    """Test cases for Leaderboard API endpoints"""
    
    def setUp(self):
        self.leaderboard = Leaderboard.objects.create(
            user_email='leader@test.com',
            user_name='Top Hero',
            team='Test Team',
            total_points=500,
            total_activities=10,
            rank=1
        )
    
    def test_get_leaderboard(self):
        """Test retrieving leaderboard"""
        response = self.client.get('/api/leaderboard/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_top_leaderboard(self):
        """Test retrieving top 10 from leaderboard"""
        response = self.client.get('/api/leaderboard/top/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
