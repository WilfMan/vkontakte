/**
 * Created by wilfman on 5/26/15.
 */

function getUrlList() {
    var list = document.querySelectorAll('div.audio.fl_l');
    var files = [];
    for (var i = 0; i < list.length; i++) {
        var tel = list[i];
        var group = tel.querySelector('.title_wrap').querySelector('b').innerText;
        var name = tel.querySelector('.title_wrap').querySelector('.title').innerText;
        var f_url = tel.querySelector('input').value;
        files.push(JSON.stringify({
            url: f_url,
            artist: group,
            title: name
        }));
    }
    var a = document.createElement('a');
    a.download = 'vk_music.txt';
    var oUrl = URL.createObjectURL(new Blob([files.join("\n")], {type: 'text/plain'}));
    a.href = oUrl;
    a.click();
    delete a;
    URL.revokeObjectURL(oUrl);
}

var scrollTop = -1;
var iv = setInterval( function() {
    if (document.body.scrollTop > scrollTop) {
        scrollTop = document.body.scrollTop;
        document.body.scrollTop = scrollTop + 10000;
    } else {
      clearInterval(iv);
      getUrlList();
    }
}, 1000);