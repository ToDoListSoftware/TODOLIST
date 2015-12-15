/**
 * Created by ryan on 15/12/16.
 */
window.onload=function(){
    var a = document.getElementById('wanttosearch');
    alert(a.value);
    if(a.value){
        var b = document.getElementById('startsearch');
        b.disabled = true;
    }
    else{
        b.disabled = false;
    }
}