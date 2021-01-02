document.addEventListener('DOMContentLoaded', function() {


  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#details-page').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#details-page').style.display = 'none';
  document.querySelector('#emails-view').style.display = 'block';
  // console.log(mailbox);
  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
    send(mailbox);
}

function OnComposeSubmit(){
    var tousername = document.getElementById("compose-recipients").value;
    var sub = document.getElementById("compose-subject").value;
    var body = document.getElementById("compose-body").value;
    fetch("/emails", {
      method: "POST",
      body: JSON.stringify({
        recipients: tousername, 
        subject: sub,
        body: body})
      })
      .then(response =>response.json())
      .then(function(res){
        console.log(res);
      });
}

function send(forwhat){
  var req = new XMLHttpRequest();
  req.open("GET", "emails/"+forwhat);
  req.onload = ()=>{
    var result = JSON.parse(req.responseText);  
    // console.log(result);
    var emailview = document.getElementById("emails-view");
    result.forEach(element => {
      var email = document.createElement("div");
      var childemail = document.createElement("div");
      email.appendChild(childemail);
      childemail.classList.add("email");
      childemail.id = element.id;
      if(element.read == true){
        childemail.style.backgroundColor = "rgb(212,212,212)";
      }
      var div_from = document.createElement("div");
      var title = document.createElement("div");
      var date_div = document.createElement("div");

      var btn = document.createElement("button");
      btn.style.backgroundColor = "red";
      btn.style.color = "white";
      btn.style.borderRadius = '5px';
      btn.style.width = "5.5em";
      btn.style.float = "right";
      btn.style.borderWidth = "1px";
      btn.style.boxShadow= "0";
      var btn_div = document.createElement("div");
      btn_div.appendChild(btn);

      

      
      

      childemail.appendChild(div_from);
      childemail.appendChild(title);
      childemail.appendChild(date_div);

      var date = document.createElement("span");
      date_div.appendChild(date);
      div_from.style.fontWeight = "bold";
      date.style.color = "gray";
      childemail.style.border = "1px solid black";
      childemail.style.padding = "5px";
      childemail.style.display = "grid";
      date.style.float = "right";
      if(forwhat == "inbox" || forwhat == "archive"){
        childemail.appendChild(btn_div);
        childemail.style.gridTemplateColumns = "1fr 2fr 1fr 1fr";
      }else{
        
        childemail.style.gridTemplateColumns = "2fr 1fr 1fr";
      }
      
      
      if(forwhat == "inbox"|| forwhat == "archive"){
        div_from.innerHTML = element.sender;
      }else if(forwhat == "sent"){
        if(element.recipients.length = 1){
          div_from.innerHTML = element.recipients[0];
        }
      }    
      
      if(childemail.read == true){
        childemail.style.backgroundColor = "gray";
      }
      
      title.innerHTML = element.subject;
      date.innerHTML = element.timestamp;
      emailview.appendChild(email);

      // make the cursor a pointer on hover
      childemail.onmouseover = ()=>{
        childemail.style.cursor = "pointer";
        childemail.style.boxShadow = "5px 5px 5px 5px ";
        childemail.style.position = 'relative';
        childemail.style.margin = "0px -10px 0px 10px";
        
      };
      childemail.onmouseleave = ()=>{
        childemail.style.boxShadow = "0 0 0 0"; 
        childemail.style.margin = "0 0 0 0";
      };

      

      date_div.onclick = ()=>{childclick(childemail.id);};
      div_from.onclick = ()=>{childclick(childemail.id);};
      title.onclick = ()=>{childclick(childemail.id);};
      
      if(element.archived == false){
        btn.innerHTML = "Archived"
        btn.onclick = ()=>{
          fetch("emails/"+element.id, {
            method: 'PUT',
            body: JSON.stringify({
              archived: true
          })        
          });
          location.reload();
        };
      }else{
        btn.innerHTML = "Unachived"
        btn.onclick = ()=>{
          fetch("emails/"+element.id, {
            method: 'PUT',
            body: JSON.stringify({
              archived: false
          })        
          });  
          location.reload();
        };         
      }
    });
    
  };
  var data = new FormData();
  req.send(data);
}

function childclick(childemailid){
        fetch("/emails/"+childemailid, {
          method: "PUT",
          body:JSON.stringify({
            read:true
          })
        }).
        then(response=>response.text()).
        then();
        //get the details of the email 

        fetch("emails/"+childemailid)
        .then(response=>response.json())
        .then(email=>{
          console.log(email);

          // email details page
          document.querySelector('#emails-view').style.display = 'none';
          document.querySelector('#compose-view').style.display = 'none';
          document.querySelector('#details-page').style.display = 'block';

          var emailTitle = document.querySelector("#email-title");
          var emailFrom = document.querySelector("#email-from");
          var emailTo = document.querySelector("#email-to");
          var emailBody = document.querySelector("#email-body");
          var time = document.querySelector("#time");

          emailTitle.innerHTML = email.subject;
          emailTo.innerHTML ="To:"+ email.recipients[0];
          emailFrom.innerHTML = "From:" + email.sender;
          emailBody.value = email.body;
          time.innerHTML = email.timestamp;
        });

}

function replybtnclick(){
  // console.log("reply btn click");
  var fromemail = document.getElementById("email-from").innerHTML;
  email = fromemail.replace("From:", "");
  console.log(email);
  var emailsub = document.getElementById("email-title").innerHTML;
  var bodytxt = document.getElementById("email-body").value;
  var date = document.getElementById("time").innerHTML;


  console.log("from: "+email+"\nsub: "+emailsub+"\nbody: "+bodytxt);
  compose_email();
  document.querySelector('#compose-recipients').value = email;
  if(emailsub.substring(0,4) == "Re: "){
    document.querySelector('#compose-subject').value = emailsub;
  }else{
    document.querySelector('#compose-subject').value = "Re: "+emailsub;
  }
  document.querySelector('#compose-body').value = "On "+date+"\n"+email+"\n\nWrote: "+bodytxt;
  document.getElementById('compose-recipients').disabled = true;
}