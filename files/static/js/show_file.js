function getFileMimeType(url, callback) {
	var xmlhttp = new XMLHttpRequest();

	xmlhttp.onreadystatechange = function() {
		if (xmlhttp.readyState === XMLHttpRequest.DONE) {
			var mime_type = xmlhttp.getResponseHeader("content-type");
			callback(mime_type);
		} else {
			callback();
		}
	};
	xmlhttp.open("HEAD", url, false);
	xmlhttp.send();
}

function downloadFile(url, callback) {
	var xmlhttp = new XMLHttpRequest();

	xmlhttp.onreadystatechange = function() {
		if (xmlhttp.readyState === XMLHttpRequest.DONE) {
			callback(xmlhttp.responseText);
		} else {
			callback();
		}
	};
	xmlhttp.open("GET", url, false);
	xmlhttp.send();

}

function showFileContent() {
	var f_input = document.getElementById('f-select'),
		f_url = f_input.value,
		content_div = document.getElementById('f-content');
	getFileMimeType(f_url, function (mime_type) {
		if (mime_type.indexOf('text') !== -1) {
			downloadFile(f_url, function (loaded_file) {
				content_div.innerHTML = '<pre>'+loaded_file+'</pre>';
			});
		} else if (mime_type.indexOf('image') !== -1) {
			content_div.innerHTML = '<img src="'+ f_url +'" />'
		} else {
			content_div.innerText = 'Формат файла не поддерживается';
		}
	});
}

/* Обработка событий */
document.addEventListener('DOMContentLoaded', function() {

	var show_btn = document.getElementById('f-show-btn');
	show_btn.addEventListener('click', showFileContent, false);

	showFileContent();
});
