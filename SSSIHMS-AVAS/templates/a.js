
function changecolor() {
	var name = document.getElementById("txt_fname").value.trim();
	var pswd = document.getElementById("txt_pswd").value.trim();
	if(name!="" && pswd!="")
	{
		document.getElementById("btn_submit").style.background='#00ff27';
	}
	else
	{
		document.getElementById("btn_submit").style.background='#ff0000';
	}

}

