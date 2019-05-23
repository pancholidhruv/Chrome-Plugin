// This callback function is called when the content script has been
// injected and returned its results
function onPageDetailsReceived(pageDetails) {
    document.getElementById('title').value = pageDetails.title;
    document.getElementById('url').value = pageDetails.url;
    var url_string = new URL(pageDetails.url);
    var query = url_string.searchParams.get("q");
    document.getElementById('query').value = "www.flipkart.com?search=" + query;

    // if(query != null){
    //     chrome.tabs.create({url:"typedUrls.html"});
    // }
}

// Global reference to the status display SPAN
var statusDisplay = null;

// POST the data to the server using XMLHttpRequest
function addBookmark() {
    // Cancel the form submit
    event.preventDefault();

    // The URL to POST our data to
    var postUrl = 'http://post-test.local.com';

    // Set up an asynchronous AJAX POST request
    var xhr = new XMLHttpRequest();
    xhr.open('POST', postUrl, true);

    // Prepare the data to be POSTed by URLEncoding each field's contents
    var title = document.getElementById('title');
    var url = document.getElementById('url');
    var summary = document.getElementById('summary');
    var tags = document.getElementById('tags');
    var params = 'title=' + encodeURIComponent(title.value) +
        '&url=' + encodeURIComponent(url.value) +
        '&summary=' + encodeURIComponent(summary.value) +
        '&tags=' + encodeURIComponent(tags.value);

    // Replace any instances of the URLEncoded space char with +
    params = params.replace(/%20/g, '+');

    // Set correct header for form data
    var formContentType = 'application/x-www-form-urlencoded';
    xhr.setRequestHeader('Content-type', formContentType);

    // Handle request state change events
    xhr.onreadystatechange = function() {
        // If the request completed
        if (xhr.readyState == 4) {
            statusDisplay.innerHTML = '';
            if (xhr.status == 200) {
                // If it was a success, close the popup after a short delay
                statusDisplay.innerHTML = 'Saved!';
                window.setTimeout(window.close, 1000);
            } else {
                // Show what went wrong
                statusDisplay.innerHTML = 'Error saving: ' + xhr.statusText;
            }
        }
    };

    // Send the request and set status
    xhr.send(params);
    statusDisplay.innerHTML = 'Saving...';
}

window.onload = function() {
    //
};

// When the popup HTML has loaded
window.addEventListener('load', function(evt) {
    // Cache a reference to the status display SPAN
    statusDisplay = document.getElementById('status-display');
    // Handle the bookmark form submit event with our addBookmark function
    document.getElementById('addbookmark')
        .addEventListener('submit', addBookmark);
    // Get the event page
    chrome.runtime.getBackgroundPage(function(eventPage) {
        // Call the getPageInfo function in the event page, passing in
        // our onPageDetailsReceived function as the callback. This
        // injects content.js into the current tab's HTML
        eventPage.getPageDetails(onPageDetailsReceived);
    });


});