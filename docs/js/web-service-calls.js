/**
	* @createdBy Govind Savara
	* @createdDate 10/4/2016
	* @lastModifiedBy Govind Savara
	* @lastModifiedDate 10/8/2016
	* @type Routine
	* @desc handles all the ajax calls
	* @param {string} url, the url to be referred
	* @return{string} returns the string returned from the ajax call
*/

function getWebserviceResponseGet(postData) {
	console.log(postData);
	$.ajax({
		url: "http://127.0.0.1:9004/links?keyword=" + postData,
		type: "GET",
		crossDomain: true,
		timeout: 200000000,
		success: function(response) {
		    request = JSON.parse(response);
            if(request["status"] == "success"){
                //data = JSON.parse(request["data"]);
                console.log("data: ", request["data"]);
                contentDisplay(request["data"]);
                pagination_function(10);
            } else {
                $("#error_display").show();
                console.log("Error");
                document.getElementById("error_display").innerHTML = request["error"];
            }


//            console.log("Error");
//            $("#error_display").show();
//            document.getElementById("error_display").innerHTML = response.error;

		},
		error: function(xhr, options, error) {
			console.log("Error occurred during processing the command in webservice post data");
		}
	});

}