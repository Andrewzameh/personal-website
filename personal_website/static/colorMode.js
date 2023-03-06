$(document).ready(function () {
	$(".toggler").click(function () {
		$(".sun-logo").toggleClass("animate-sun");
		$(".moon-logo").toggleClass("animate-moon");
		$("body").attr("data-bs-theme", function (index, attr) {
			return attr == "dark" ? "light" : "dark";
		});
		$(".myLogo").attr("src", function (index, attr) {
			return attr == "../static/images/logo-black.svg"
				? "../static/images/logo-white.svg"
				: "../static/images/logo-black.svg";
		});
	});
});
