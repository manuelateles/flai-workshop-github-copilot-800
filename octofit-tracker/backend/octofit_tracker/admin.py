from django.contrib import admin
from .models import User, Team, Activity, Leaderboard, Workout


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'team', 'created_at')
    list_filter = ('team', 'created_at')
    search_fields = ('name', 'email')
    ordering = ('-created_at',)


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'members_count', 'total_points', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name',)
    ordering = ('-total_points',)
    readonly_fields = ('created_at',)


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ('user_email', 'activity_type', 'duration', 'calories_burned', 'points', 'date')
    list_filter = ('activity_type', 'date')
    search_fields = ('user_email', 'activity_type')
    ordering = ('-date',)
    readonly_fields = ('created_at',)


@admin.register(Leaderboard)
class LeaderboardAdmin(admin.ModelAdmin):
    list_display = ('rank', 'user_name', 'team', 'total_points', 'total_activities', 'updated_at')
    list_filter = ('team',)
    search_fields = ('user_name', 'user_email')
    ordering = ('rank',)
    readonly_fields = ('updated_at',)


@admin.register(Workout)
class WorkoutAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'difficulty', 'duration', 'calories_per_session', 'points_per_session')
    list_filter = ('type', 'difficulty')
    search_fields = ('name', 'description')
    ordering = ('name',)
    readonly_fields = ('created_at',)
