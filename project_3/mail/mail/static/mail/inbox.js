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
  document.querySelector("#back-button").addEventListener("click", () => {
    email_view = document.querySelector("#full-email-view");
    email_view.style.display = "none";
    document.querySelector("#emails-view").style.zindex = "10";
  });
  document.querySelector("#reply-button").addEventListener("click", () => {
    reply_email(email_id);
  });
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
  }).then((response) => response.json());

  load_mailbox("sent");
}

function compose_email() {
  // Show compose view and hide other views
  document.querySelector("#emails-view").style.display = "none";
  document.querySelector("#full-email-view").style.display = "none";
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

function reply_email(email_id) {
  fetch(`/emails/${email_id}`)
    .then((response) => response.json())
    .then((email) => {
      compose_email();
      document.querySelector("#compose-recipients").value = email.sender;
      document.querySelector("#compose-subject").value = `Re: ${email.subject}`;
      document.querySelector("#compose-body").value = `
      On ${email.timestamp}, ${email.sender} wrote:
      ${email.body}
      `;
    });
}

function archive_email(email_id, archived) {
  fetch(`/emails/${email_id}`, {
    method: "PUT",
    body: JSON.stringify({
      archived: !archived,
    }),
  });
  load_mailbox("inbox");
}

function read_email(email_id) {
  fetch(`/emails/${email_id}`)
    .then((response) => response.json())
    .then((email) => {
      document.querySelector("#full-email-view").style.display = "none";
      document.querySelector("#full-email-view").style.display = "block";
      document.querySelector("#emails-view").style.zindex = "-10";
      back_button = document.querySelector("#back-button");

      email_view = document.querySelector("#full-email-view");
      email_view.innerHTML = `
      <div class="full-email">
        <div class="full-email-header">
          <span class="full-email-subject">${email.subject}</span>
          <div class="full-email-subheader">
            <span class="full-email-sender">${email.sender}</span>
            <span class="full-email-date">${email.timestamp}</span>
          </div>
        </div>
        <div class="full-email-body" type="box">${email.body}</div>
        <div class="full-email-footer">
        <button class="btn btn-primary" id="reply-button">Reply</button>
        <button class="btn btn-danger" id="archive-button">Archive</button>
        </div>
      </div>
      `;
      email_view.appendChild(back_button);

      if (email.archived) {
        document.querySelector("#archive-button").innerHTML = "Unarchive";
      }
      document.querySelector("#archive-button");

      document
        .querySelector("#archive-button")
        .addEventListener("click", () => {
          archive_email(email_id, email.archived);
        });
      document.querySelector("#reply-button").addEventListener("click", () => {
        reply_email(email_id);
      });
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
  document.querySelector("#full-email-view").style.display = "none";

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
    });

  // Show the mailbox name
  document.querySelector("#emails-view").innerHTML = `<h3>${
    mailbox.charAt(0).toUpperCase() + mailbox.slice(1)
  }</h3>`;
}
