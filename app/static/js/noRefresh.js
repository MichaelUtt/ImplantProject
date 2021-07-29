$(function() {
    $('a#add_implant').bind('click', function() {
        var new_implant = document.getElementById("add_implant_text").value;

        var option = document.createElement("option");
        option.text = new_implant;
        var implant_n = document.getElementById("implants").getElementsByTagName("option").length;
        option.value = implant_n + 1;
        var select = document.getElementById("implants");
        select.appendChild(option);

        $.getJSON('/add_implant/' + new_implant,
            function() {
        });
        return false;
    });
});

$(function() {
    $('a#add_cap').bind('click', function() {
        var new_cap = document.getElementById("add_cap_text").value;

        var option = document.createElement("option");
        option.text = new_cap;
        var implant_n = document.getElementById("healingcaps").getElementsByTagName("option").length;
        option.value = implant_n + 1;
        var select = document.getElementById("healingcaps");
        select.appendChild(option);

        $.getJSON('/add_cap/' + new_cap,
            function(data) {
        });
        return false;
    });
});

$(function() {
    $('a#add_part').bind('click', function() {
        var new_part = document.getElementById("add_part_text").value;

        var option = document.createElement("option");
        option.text = new_part;
        var implant_n = document.getElementById("restorativeparts").getElementsByTagName("option").length;
        option.value = implant_n + 1;
        var select = document.getElementById("restorativeparts");
        select.appendChild(option);

        $.getJSON('/add_part/' + new_part,
            function(data) {
        });
        return false;
    });
});

$(function() {
    $('.remove_btn').bind('click', function() {
        var btnId = this.id;

        var btnIdSplice = btnId.split("-");
        var optVal = btnIdSplice[2];
        var optTable = btnIdSplice[1];

        if (optTable == "implants") {
            var implantOpts = document.querySelectorAll("ul#implants > li");
            var old_implant = implantOpts[parseInt(optVal-1)].childNodes[2];
            console.log(old_implant.innerHTML);
            $.getJSON('/remove_implant/' + old_implant.innerHTML,
                function() {
                });
            return false;

        } else if (optTable == "healingcaps") {
            $.getJSON('/remove_cap/' + new_implant,
                function() {
                });
            return false;

        }  else if (optTable == "restorativeparts") {
            $.getJSON('/remove_part/' + new_implant,
                function() {
                });
            return false;

        }
        var new_implant = "a";
        $.getJSON('/add_implant/' + new_implant,
            function() {
        });
        return false;

    });
});



var allOptions = document.querySelectorAll("ul.select-checkbox > li");
var parentDiv = allOptions[0].parentElement;
var j = 0;
for (let i = 0; i < allOptions.length; i++) {
    var deleteOption = document.createElement("button");
    deleteOption.type = "submit";
    deleteOption.className = "remove_btn";
    deleteOption.innerHTML = "X";
    j = j + 1;
    if (parentDiv != allOptions[i].parentElement) {
        parentDiv = allOptions[i].parentElement;
        j = 1;
    }
    var temp_id = "delete-"+parentDiv.id+"-"+j;
    deleteOption.id = temp_id;
    //console.log(deleteOption);
    allOptions[i].appendChild(deleteOption);
    //parentDiv.insertBefore(deleteOption, allOptions[i]);

}

