function endOfDayButton() {
    var $poIDs = $('.table th');
    var poIDs = {};
    $poIDs.each(function () {
        if (this.innerText !== "Task") {
            poIDs[this.className] = this.innerText.split(' - ')[1];
        }
    });

    var data = [];
    var keyCount = Object.keys(poIDs).length;
    for (var i = 0; i < keyCount; i++) {
        var col = $('.col'+i+' input');
        var temp = {
            "id": poIDs['col'+i],
            "nums": []
        };
        for (var j = 0; j < col.length; j++) {
            temp['nums'].push(col[j].value === '' ? "0" : col[j].value);
        }
        data.push(temp);
    }

    $.ajax({
        type: 'POST',
        url: 'temp',
        data: JSON.stringify(data),
        dataType: 'json'
    })
}