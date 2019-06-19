var Rainbow = function(){
	if (this.i < 360) {
		var step = this.i % 360;
		this.i++;
	}else this.i = 0;

	return "hsl(" + step + ", 100%, 50% )";
}

var setRainbowColor = function(id){
			var i = 0;

			r = Rainbow.bind(this)

			setInterval(function(){
				document.getElementById(id).style.color = r()
			}, 50);
};

var setRainbowBorderColor = function(id){
			var i = 0;

			r = Rainbow.bind(this)

			setInterval(function(){
				document.getElementById(id).style.borderColor = r()
			}, 50);
};


var setRainbowBackgroundColor = function(id){
			var i = 0;

			r = Rainbow.bind(this)

			setInterval(function(){
				document.getElementById(id).style.backgroundColor = r()
			}, 50);
};


var rain = function(id){
	var i = 0;

			var Rainbow = function(){
				if (i < 360) {
					var step = i % 360;
                    i++;
				}else i = 0;

				return "hsl(" + step + ", 100%, 50% )";
			}
			setInterval(function(){
				document.getElementById(id).style.borderColor = Rainbow()
				document.getElementById(id).style.color = Rainbow()
				document.getElementById(id).style.backgroundColor = Rainbow()
			}, 50);
};
