var selected = [];
var immagine = [];
function printQrCodes() {
    selected = getIdSelections();
    console.log(selected.toString());
    makeQR(selected);
    printDiv();
}

function printSingleQrCode(id) {
    selected.push(id);
    makeQR(selected);
    printDiv();
    selected = []
}

function printDiv(text) {
    var printContents = "";
    for(var i=0;i<immagine.length; i++)
    {
        printContents += immagine[i];
        i++;
        printContents += immagine[i];
    }
    console.log(printContents);
    var winPrint = window.open('', '', 'left=0,top=0,width=800,height=600,toolbar=0,scrollbars=0,status=0');
    winPrint.document.write(printContents);
    winPrint.document.close();
    winPrint.focus();
    winPrint.print();
    winPrint.close(); 
}

function makeQR(text) {
    $("#qrcode").empty();
    immagine = [];
    img = [];
    for (var i = 0; i < text.length; i++) {
        var text1 = text[i];
        var url = document.location.origin + '/inventario/show/'+ text1 +'/';
        console.log(url);
        jQuery(function () {
                    $("#qrcode").qrcode({
                        text: url,
                        render: 'canvas',
                        size: 100
                    });
                    var canvas = $('#qrcode canvas');
                    console.log(canvas);
                    var img1 = canvas.get(i).toDataURL('image/png');
                    immagine.push('<div style="float:left;padding: 10px"><img src="' + img1 + '"/><br><span>' + text1 + '</span></div>');
                    console.log(immagine[i]);
                }
        );
    }
}