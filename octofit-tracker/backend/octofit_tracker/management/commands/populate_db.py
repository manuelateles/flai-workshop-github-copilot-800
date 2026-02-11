from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from octofit_tracker.models import User, Team, Activity, Leaderboard, Workout


class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Deleting existing data...')
        
        # Delete all existing data
        User.objects.all().delete()
        Team.objects.all().delete()
        Activity.objects.all().delete()
        Leaderboard.objects.all().delete()
        Workout.objects.all().delete()
        
        self.stdout.write(self.style.SUCCESS('Existing data deleted.'))
        
        # Create Teams
        self.stdout.write('Creating teams...')
        team_marvel = Team.objects.create(
            name='Team Marvel',
            description='Heroes from the Marvel Universe',
            members_count=0,
            total_points=0
        )
        
        team_dc = Team.objects.create(
            name='Team DC',
            description='Heroes from the DC Universe',
            members_count=0,
            total_points=0
        )
        
        self.stdout.write(self.style.SUCCESS('Teams created.'))
        
        # Create Users (Superheroes)
        self.stdout.write('Creating users...')
        
        marvel_users = [
            {'name': 'Iron Man', 'email': 'ironman@marvel.com'},
            {'name': 'Captain America', 'email': 'capamerica@marvel.com'},
            {'name': 'Thor', 'email': 'thor@marvel.com'},
            {'name': 'Black Widow', 'email': 'blackwidow@marvel.com'},
            {'name': 'Hulk', 'email': 'hulk@marvel.com'},
            {'name': 'Spider-Man', 'email': 'spiderman@marvel.com'},
        ]
        
        dc_users = [
            {'name': 'Superman', 'email': 'superman@dc.com'},
            {'name': 'Batman', 'email': 'batman@dc.com'},
            {'name': 'Wonder Woman', 'email': 'wonderwoman@dc.com'},
            {'name': 'Flash', 'email': 'flash@dc.com'},
            {'name': 'Aquaman', 'email': 'aquaman@dc.com'},
            {'name': 'Green Lantern', 'email': 'greenlantern@dc.com'},
        ]
        
        created_users = []
        
        for user_data in marvel_users:
            user = User.objects.create(
                name=user_data['name'],
                email=user_data['email'],
                team='Team Marvel'
            )
            created_users.append(user)
        
        for user_data in dc_users:
            user = User.objects.create(
                name=user_data['name'],
                email=user_data['email'],
                team='Team DC'
            )
            created_users.append(user)
        
        # Update team member counts
        team_marvel.members_count = len(marvel_users)
        team_marvel.save()
        team_dc.members_count = len(dc_users)
        team_dc.save()
        
        self.stdout.write(self.style.SUCCESS(f'Created {len(created_users)} users.'))
        
        # Create Workouts
        self.stdout.write('Creating workouts...')
        
        workouts_data = [
            {
                'name': 'Super Strength Training',
                'description': 'Build incredible strength with this intense workout',
                'type': 'Strength',
                'difficulty': 'Hard',
                'duration': 60,
                'calories_per_session': 500,
                'points_per_session': 50
            },
            {
                'name': 'Speed Running',
                'description': 'Improve your speed with high-intensity interval training',
                'type': 'Cardio',
                'difficulty': 'Medium',
                'duration': 30,
                'calories_per_session': 350,
                'points_per_session': 35
            },
            {
                'name': 'Flexibility & Balance',
                'description': 'Enhance flexibility and balance with yoga-inspired movements',
                'type': 'Flexibility',
                'difficulty': 'Easy',
                'duration': 45,
                'calories_per_session': 200,
                'points_per_session': 25
            },
            {
                'name': 'Combat Training',
                'description': 'Mixed martial arts inspired workout',
                'type': 'Combat',
                'difficulty': 'Hard',
                'duration': 75,
                'calories_per_session': 600,
                'points_per_session': 60
            },
            {
                'name': 'Endurance Run',
                'description': 'Long-distance running for stamina building',
                'type': 'Cardio',
                'difficulty': 'Medium',
                'duration': 90,
                'calories_per_session': 700,
                'points_per_session': 70
            },
            {
                'name': 'Power Lifting',
                'description': 'Heavy weightlifting for maximum strength',
                'type': 'Strength',
                'difficulty': 'Hard',
                'duration': 60,
                'calories_per_session': 450,
                'points_per_session': 55
            },
        ]
        
        created_workouts = []
        for workout_data in workouts_data:
            workout = Workout.objects.create(**workout_data)
            created_workouts.append(workout)
        
        self.stdout.write(self.style.SUCCESS(f'Created {len(created_workouts)} workouts.'))
        
        # Create Activities
        self.stdout.write('Creating activities...')
        
        activity_types = [
            'Super Strength Training',
            'Speed Running',
            'Flexibility & Balance',
            'Combat Training',
            'Endurance Run',
            'Power Lifting'
        ]
        
        created_activities = []
        for i, user in enumerate(created_users):
            # Create 3-5 activities per user from the past week
            num_activities = 3 + (i % 3)
            for j in range(num_activities):
                days_ago = j * 2
                activity_type = activity_types[j % len(activity_types)]
                
                # Find matching workout for points calculation
                workout = next((w for w in created_workouts if w.name == activity_type), None)
                
                activity = Activity.objects.create(
                    user_email=user.email,
                    activity_type=activity_type,
                    duration=workout.duration if workout else 45,
                    calories_burned=workout.calories_per_session if workout else 300,
                    points=workout.points_per_session if workout else 30,
                    date=timezone.now() - timedelta(days=days_ago)
                )
                created_activities.append(activity)
        
        self.stdout.write(self.style.SUCCESS(f'Created {len(created_activities)} activities.'))
        
        # Create Leaderboard entries
        self.stdout.write('Creating leaderboard...')
        
        leaderboard_entries = []
        for user in created_users:
            # Calculate user's total points from activities
            user_activities = Activity.objects.filter(user_email=user.email)
            total_points = sum(activity.points for activity in user_activities)
            total_activities = user_activities.count()
            
            leaderboard = Leaderboard.objects.create(
                user_email=user.email,
                user_name=user.name,
                team=user.team,
                total_points=total_points,
                total_activities=total_activities,
                rank=0  # Will be calculated after all entries are created
            )
            leaderboard_entries.append(leaderboard)
        
        # Sort by total_points and assign ranks
        leaderboard_entries.sort(key=lambda x: x.total_points, reverse=True)
        for rank, entry in enumerate(leaderboard_entries, start=1):
            entry.rank = rank
            entry.save()
        
        # Update team total points
        marvel_points = sum(entry.total_points for entry in leaderboard_entries if entry.team == 'Team Marvel')
        dc_points = sum(entry.total_points for entry in leaderboard_entries if entry.team == 'Team DC')
        
        team_marvel.total_points = marvel_points
        team_marvel.save()
        team_dc.total_points = dc_points
        team_dc.save()
        
        self.stdout.write(self.style.SUCCESS(f'Created {len(leaderboard_entries)} leaderboard entries.'))
        
        # Summary
        self.stdout.write(self.style.SUCCESS('\n=== Database Population Complete ==='))
        self.stdout.write(self.style.SUCCESS(f'Teams: {Team.objects.count()}'))
        self.stdout.write(self.style.SUCCESS(f'Users: {User.objects.count()}'))
        self.stdout.write(self.style.SUCCESS(f'Workouts: {Workout.objects.count()}'))
        self.stdout.write(self.style.SUCCESS(f'Activities: {Activity.objects.count()}'))
        self.stdout.write(self.style.SUCCESS(f'Leaderboard Entries: {Leaderboard.objects.count()}'))
        self.stdout.write(self.style.SUCCESS(f'\nTeam Marvel: {team_marvel.members_count} members, {team_marvel.total_points} points'))
        self.stdout.write(self.style.SUCCESS(f'Team DC: {team_dc.members_count} members, {team_dc.total_points} points'))
