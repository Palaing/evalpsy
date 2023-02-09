<!DOCTYPE html>
<html lang="fr">
<head>
	<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
	<title>{{titre}}</title>
	<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css" integrity="sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO" crossorigin="anonymous">
	<style>
	.serre {
	  line-height: 80%;
	}
	</style>
</head>
<body>
<div class="container" style="max-width: 720px;">
	<div class="row mb-4 serre">
		<div class="col center"><h3>{{titre}}</h3></div>
		<div class="col-sm-3 text-decoration-none text-right serre">
			<b>{{user['prenom']}}</b><br>
			<a href="/show" class="text-info">liste des participants</a><br>
			<a href="/add" class="text-warning">ajout de participants</a><br>
		% if user['isadmin']:
			<a href="/showprat" class="text-info">liste des praticiens</a><br>
			<a href="/addprat" class="text-warning">ajout de praticiens</a><br>
		% end
			<a href="/logout" class="text-secondary">déconnexion</a>
		</div>
	</div>
	% if get('message'):
	<div class="row mb-4 alert alert-danger justify-content-center" role="alert">{{message}}</div>
	% end			
</div>
</body>
</html>
