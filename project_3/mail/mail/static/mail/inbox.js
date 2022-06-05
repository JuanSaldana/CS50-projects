document.addEventListener("DOMContentLoaded", function () {
  // Use buttons to toggle between views
  document
    .querySelector("#inbox")
    .addEventListener("click", () => load_mailbox("inbox"));
  document
    .querySelector("#sent")
    .addEventListener("click", () => load_mailbox("sent"));
  document
    .querySelector("#archived")
    .addEventListener("click", () => load_mailbox("archive"));
  document.querySelector("#compose").addEventListener("click", compose_email);

  // By default, load the inbox
  load_mailbox("inbox");
});

function send_email(event) {
  event.preventDefault();
  console.log("Sending...");
  recipients = document.querySelector("#compose-recipients").value;
  subject = document.querySelector("#compose-subject").value;
  body = document.querySelector("#compose-body").value;
  email = JSON.stringify({
    recipients: recipients,
    subject: subject,
    body: body,
  });

  fetch("/emails", {
    method: "POST",
    body: email,
  })
    .then((response) => response.json())
    .then((result) => {
      console.log(result);
    });

  load_mailbox("sent");
}

function compose_email() {
  // Show compose view and hide other views
  document.querySelector("#emails-view").style.display = "none";
  document.querySelector("#compose-view").style.display = "block";

  // Clear out composition fields
  document.querySelector("#compose-recipients").value = "";
  document.querySelector("#compose-subject").value = "";
  document.querySelector("#compose-body").value = "";

  // Send mail on submit
  document
    .querySelector("#compose-form")
    .addEventListener("submit", send_email);
}

function read_email(email_id) {
  console.log(email_id);
  fetch(`/emails/${email_id}`)
    .then((response) => response.json())
    .then((email) => {
      console.log(email);
      document.querySelector("#email-view").style.display = "block";
      document.querySelector("#emails-view").style.display = "none";

      email_view = document.querySelector("#email-view");
      email_view.innerHTML = `
      <div class="full-email-header">
      <span class="full-email-subject">${email.subject}</span>
      <div class="full-email-subheader">
      <span class="full-email-sender">${email.sender}</span>
        <span class="full-email-date">${email.timestamp}</span>
      </div>
        <div class="full-email-body" type="box">${email.body}</div>
      `;
    });

  fetch(`/emails/${email_id}`, {
    method: "PUT",
    body: JSON.stringify({
      read: true,
    }),
  });
}

function load_mailbox(mailbox) {
  // Show the mailbox and hide other views
  document.querySelector("#emails-view").style.display = "block";
  document.querySelector("#compose-view").style.display = "none";
  document.querySelector("#email-view").style.display = "none";

  // Query emails
  fetch(`/emails/${mailbox}`)
    .then((response) => response.json())
    .then((result) => {
      emails_view = document.querySelector("#emails-view");
      for (email of result) {
        emails_view.innerHTML += `
        <hr class="email-hr">
        <div class="email" read=${email.read} id=${email.id}>
        <div class="email-header">
          <span class="email-subject">${email.subject}</span>
          <div class="email-subheader">
            <span class="email-date">${email.timestamp}</span>
            <span class="email-sender">${email.sender}</span>
          </div>
        </div>
        <div class="email-body">${email.body}</div>
      </div>
        `;
      }

      // Add event listeners to each email
      for (email of document.querySelectorAll(".email")) {
        email_id = email.getAttribute("id");
        email.addEventListener("click", read_email.bind(null, email_id));
      }
      console.log(result);
    });

  // Show the mailbox name
  document.querySelector("#emails-view").innerHTML = `<h3>${
    mailbox.charAt(0).toUpperCase() + mailbox.slice(1)
  }</h3>`;
}
