import React, { useState, useEffect } from 'react';

function Workouts() {
  const [workouts, setWorkouts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const apiUrl = `https://${process.env.REACT_APP_CODESPACE_NAME}-8000.app.github.dev/api/workouts/`;
    console.log('Workouts API endpoint:', apiUrl);
    
    fetch(apiUrl)
      .then(response => {
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
      })
      .then(data => {
        console.log('Workouts fetched data:', data);
        // Handle both paginated (.results) and plain array responses
        const workoutsData = data.results || data;
        setWorkouts(Array.isArray(workoutsData) ? workoutsData : []);
        setLoading(false);
      })
      .catch(error => {
        console.error('Error fetching workouts:', error);
        setError(error.message);
        setLoading(false);
      });
  }, []);

  if (loading) return <div className="container mt-4"><div className="text-center"><div className="spinner-border text-primary" role="status"><span className="visually-hidden">Loading...</span></div><p className="mt-2">Loading workouts...</p></div></div>;
  if (error) return <div className="container mt-4"><div className="alert alert-danger" role="alert"><strong>Error:</strong> {error}</div></div>;

  return (
    <div className="container mt-4">
      <h2>💪 Workout Suggestions</h2>
      {workouts.length === 0 ? (
        <div className="alert alert-info" role="alert">No workout suggestions found.</div>
      ) : (
        <div className="row">
          {workouts.map((workout) => {
            let difficultyBadge = 'bg-secondary';
            if (workout.difficulty === 'Easy' || workout.difficulty === 'Beginner') difficultyBadge = 'bg-success';
            else if (workout.difficulty === 'Medium' || workout.difficulty === 'Intermediate') difficultyBadge = 'bg-warning';
            else if (workout.difficulty === 'Hard' || workout.difficulty === 'Advanced') difficultyBadge = 'bg-danger';
            
            return (
              <div key={workout.id} className="col-md-6 mb-4">
                <div className="card h-100">
                  <div className="card-header">
                    <h5 className="card-title mb-0">{workout.name}</h5>
                  </div>
                  <div className="card-body">
                    {workout.description && (
                      <p className="card-text">{workout.description}</p>
                    )}
                    <div className="d-flex flex-wrap gap-2">
                      {workout.duration && (
                        <span className="badge bg-primary">⏱️ {workout.duration} min</span>
                      )}
                      {workout.difficulty && (
                        <span className={`badge ${difficultyBadge}`}>{workout.difficulty}</span>
                      )}
                      {workout.type && (
                        <span className="badge bg-info">{workout.type}</span>
                      )}
                    </div>
                  </div>
                  <div className="card-footer">
                    <button className="btn btn-sm btn-primary">Start Workout</button>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}

export default Workouts;
