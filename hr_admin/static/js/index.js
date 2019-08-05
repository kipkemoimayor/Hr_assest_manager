'use strict'
$(document).ready(_=>{
  let anchor=document.querySelector("#dashboard >div");
  let anchorTwo=document.querySelector("#two");
  let anchorThree=document.querySelector("#three");
  console.log(anchorTwo);
  anchor.addEventListener("click",_=>{
    anchor.classList.add("actives")
    anchorTwo.classList.remove("actives")
    anchorThree.classList.remove("actives")
  });
  anchorTwo.addEventListener("click",_=>{
    anchorTwo.classList.add("actives")
    anchor.classList.remove("actives")
    anchorThree.classList.remove("actives")
  });
  anchorThree.addEventListener("click",_=>{
    anchorThree.classList.add("actives")
    anchorTwo.classList.remove("actives")
    anchor.classList.remove("actives")
  })
});
