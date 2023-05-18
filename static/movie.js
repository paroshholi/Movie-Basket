const options = {
	method: 'GET',
	headers: {
		'X-RapidAPI-Key': '04c85b10d3msha5c5e41212b0758p110a4djsn36fc1a6cdd9a',
		'X-RapidAPI-Host': 'moviesminidatabase.p.rapidapi.com'
	}
};

fetch('https://moviesminidatabase.p.rapidapi.com/movie/imdb_id/byTitle/%7Bname%7D/', options)
	.then(response => response.json())
	.then(response => console.log(response))
	.catch(err => console.error(err));