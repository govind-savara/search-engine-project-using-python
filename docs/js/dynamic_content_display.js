function contentDisplay(data){
    $("#error_display").hide();
    len=data.length;
    document.getElementById("total_count_display").innerHTML = "Found " + len + " results";
    $.each(data, function(index){
        linktag=data[index].link;
//        console.log('link:', linktag);
        record=$('<div/>',{'class':'record'});

        activelink=$('<a href="' + linktag + '", class="tag", target="_blank" />');
        activelink.text(data[index].short_desc);


        link=$('<div/>',{'class':'link'});
        link.text(data[index].link);

        description=$('<div/>',{'class':'description'});
        description.text(data[index].description);

        newline=$('<br/>');

        record.append(newline).append(activelink).append(link).append(description);

        $("#content").append(record);
//        $("#" + link_no).wrapInner('<a href="' + data[index].link + '" />');

    });
}