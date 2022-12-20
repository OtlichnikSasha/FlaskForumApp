search_btn.onclick = function(){
    if(search_inp.value === '') return;
    return location.href = `/search/${search_inp.value}`
}