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

        // Could likely just grab parent now instead of a query
        var opts = document.querySelectorAll("ul#"+optTable+" > li");
        var old_container = opts[parseInt(optVal-1)];
        var old_val = old_container.childNodes[2];

        var r = confirm("Are you sure you want to delete "+old_val.innerHTML+"?");
        if (!r) {
            $.getJSON('/do_nothing',
                function() {
                });
            return false;
        }

        if (optTable == "implants") {

            $.getJSON('/remove_implant/' + old_val.innerHTML,
                function() {
                });
        } else if (optTable == "healingcaps") {
            $.getJSON('/remove_cap/' + old_val.innerHTML,
                function() {
                });

        }  else if (optTable == "restorativeparts") {
            $.getJSON('/remove_part/' + old_val.innerHTML,
                function() {
                });
        }
        old_container.style.visibility = "hidden";
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

$(function() {
    $('#singleStage').bind('click', function() {
        var uncoverDate = this.previousSibling.previousSibling;
        var restoreDate = document.getElementById("restoreDate");
        if (this.checked) {
            uncoverDate.disabled = true;
            restoreDate.disabled = true;
        } else {
            uncoverDate.disabled = false;
            restoreDate.disabled = false;
        }
    });
});

