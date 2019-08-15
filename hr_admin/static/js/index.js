'use strict'
$(document).ready(_=>{
  let anchor=document.querySelector("#dashboard >div");
  let anchorTwo=document.querySelector("#two");
  let anchorThree=document.querySelector("#three");
  let notification=document.querySelector("#noticate")
  anchor.addEventListener("click",_=>{
    anchor.classList.add("actives")
    anchorTwo.classList.remove("actives")
    anchorThree.classList.remove("actives")
    $("#noticate").fadeOut(2000)
    $("#noticate").hide()
    $("#asset").fadeOut(2000);
    $("#account").fadeIn(2000);
    $("#asset").hide();
  });
  anchorTwo.addEventListener("click",_=>{
    anchorTwo.classList.add("actives")
    anchor.classList.remove("actives")
    anchorThree.classList.remove("actives")
    $("#noticate").fadeOut(2000)
    $("#noticate").hide()
    $("#account").fadeOut(2000);
    $("#account").hide();
    $("#asset").fadeIn(2000);
    $("#asset").show();

  });
  anchorThree.addEventListener("click",_=>{
    anchorThree.classList.add("actives")
    anchorTwo.classList.remove("actives")
    anchor.classList.remove("actives")
    $("#account").fadeOut(2000);
    $("#account").hide();
    $("#asset").fadeOut(2000);
    $("#asset").hide();
    $("#noticate").show()
    $("#noticate").fadeIn(2000)
  });

  // ajax request

  $("#assest").submit(event=>{
    event.preventDefault()
    let form=$("#assest");
    $.ajax({
      url:'/assest/asign/',
      method:"POST",
      data:form.serialize(),
      dataType:"json",
      success:data=>{
        setTimeout(function () {
        $("#message").fadeOut()
      }, 4*1000);
        $("#message").show()
      },
      error:function(){
        $("#message_err").fadeIn(800);
        $("#message_err").show();
      },
    });
    $("#id_asset_name").val("")
  });

  //ajax get request
  let btnClick= document.querySelector("[btn-data]")
  btnClick.addEventListener("click",_=>{
    $.ajax({
      url:"/assest/admin/view/",
      method:'GET',
      dataType:'json',
      success:function (data) {
        // data.forEach(name=>{
        //   alert(name)
        // })
        var list=''
        for (let i in data){
        list+= `<ul class='group-list'><li class='list-group-item'>${i} owns <strong> ${data[i]}</strong></li></ul>`
          // list+=`</br>`
        }
        $(".list").html(list)
      },
    })
  });


  // Pusher Notifications

  var pusher = new Pusher('80de7e6b8bc917286ed8', {
  cluster: 'ap2',
  forceTLS: true
  });

  var channel = pusher.subscribe('my-channel');
  var pa=document.querySelector("#love");
  channel.bind('my-event', function(data) {
    let da=''
    for(let i in data){
      alert(data[i])
       pa.textContent=JSON.stringify(data[i])
    }
      // pa.textContent=JSON.stringify(data)
  });

  let arr=[]
  let all_list=document.querySelector('#notification');


  //making notification


});
