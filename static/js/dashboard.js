document.addEventListener('DOMContentLoaded', function() {
    fetch('/api/recent_movies')
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                console.error(data.error);
                document.getElementById('recent-movies-list').innerHTML = '<li>Error loading recent movies</li>';
            } else {
                const recentMoviesList = document.getElementById('recent-movies-list');
                recentMoviesList.innerHTML = '';
                data.forEach(movie => {
                    const listItem = document.createElement('li');
                    listItem.textContent = `${movie.name} (Directed by ${movie.director}, ${movie.year})`;
                    recentMoviesList.appendChild(listItem);
                });
            }
        })
        .catch(error => {
            console.error('Error fetching recent movies:', error);
            document.getElementById('recent-movies-list').innerHTML = '<li>Error loading recent movies</li>';
        });

    fetch('/api/user_statistics')
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                console.error(data.error);
                document.getElementById('total-users').textContent = 'Error loading total users';
                document.getElementById('total-movies').textContent = 'Error loading total movies';
                document.getElementById('recent-activity').textContent = 'Error loading recent activity';
            } else {
                document.getElementById('total-users').textContent = `Total Users: ${data.total_users}`;
                document.getElementById('total-movies').textContent = `Total Movies: ${data.total_movies}`;
                document.getElementById('recent-activity').textContent = `Recent Activity: ${data.recent_activity} new movies added this week`;
            }
        })
        .catch(error => {
            console.error('Error fetching user statistics:', error);
            document.getElementById('total-users').textContent = 'Error loading total users';
            document.getElementById('total-movies').textContent = 'Error loading total movies';
            document.getElementById('recent-activity').textContent = 'Error loading recent activity';
        });
});
