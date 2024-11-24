
// Automatically transition from the landing page to the main website
window.onload = function() {
    setTimeout(() => {
        const landingPage = document.getElementById('landing-page');
        const mainWebsite = document.getElementById('main-website');

        // Fade out the landing page
        landingPage.style.opacity = '0';
        setTimeout(() => {
            landingPage.style.display = 'none'; // Hide the landing page

            // Show the main website with animation
            mainWebsite.style.display = 'block';
            setTimeout(() => {
                mainWebsite.style.opacity = '1';
            }, 50);
        }, 1000); // Adjust the fade-out duration if needed
    }, 3000); // Set the delay before transitioning to the main website (3 seconds)
};


document.addEventListener('DOMContentLoaded', function () {
    // Initialize and show the modal
    var alertModal = new bootstrap.Modal(document.getElementById('alertModal'));
    alertModal.show();

    // Set a timeout to hide the modal after 5 seconds
    setTimeout(function () {
        alertModal.hide();
    }, 20000);
});

// Color changing animation for sections on scroll
const sections = document.querySelectorAll('.section');
const colors = []; // Example colors for each section

window.addEventListener('scroll', () => {
    let scrollPosition = window.scrollY;
    sections.forEach((section, index) => {
        let sectionTop = section.offsetTop;
        let sectionHeight = section.clientHeight;

        // Change background color when section is in view
        if (scrollPosition >= sectionTop - sectionHeight / 2 && scrollPosition < sectionTop + sectionHeight / 2) {
            section.style.backgroundColor = colors[index % colors.length];
        }
    });
});

function toggleText(textContentId, button) {
    const content = document.getElementById(textContentId);

    if (content.style.maxHeight === '100px') {
        content.style.maxHeight = content.scrollHeight + 'px';
        button.innerText = 'Show Less';
    } else {
        content.style.maxHeight = '100px';
        button.innerText = 'Show More';
    }
}

// GSAP Animation for Showing Containers
window.addEventListener('load', function() {
    const containers = document.querySelectorAll('.container-custom');

    containers.forEach((container, index) => {
        gsap.to(container, {
            duration: 1,
            opacity: 1,
            y: 0,
            delay: index * 0.5, // Delay for staggered animation
            ease: 'power2.out'
        });
    });
});

function changeImage(imageSrc) {
    document.getElementById('placeholderImage').src = imageSrc;
}

function toggleContainer(containerIndex) {
    const containers = document.querySelectorAll('.container-content');
    containers.forEach((container, index) => {
        if (index === containerIndex) {
            container.classList.toggle('active');
        } else {
            container.classList.remove('active');
        }
    });
}

document.getElementById('toggleButton').addEventListener('click', function() {
    let button = this;
    let moreContent = document.getElementById('moreContent');

    if (moreContent.classList.contains('show')) {
        button.innerHTML = 'Show More';
    } else {
        button.innerHTML = 'Show Less';
    }
});

document.addEventListener('contextmenu', function (e) {
    e.preventDefault();
});

document.addEventListener('keydown', function (e) {
    if (e.key === "F12" || 
        (e.ctrlKey && e.shiftKey && e.key === 'I') || 
        (e.ctrlKey && e.shiftKey && e.key === 'J') || 
        (e.ctrlKey && e.key === 'U')) {
        e.preventDefault();
    }
});

(function () {
    function detectDevTools() {
        const devtools = /./;
        devtools.toString = function () {
            this.opened = true;
        };
        console.log(devtools);
    }
    setInterval(detectDevTools, 1000);
})();

document.addEventListener('mousedown', function (e) {
    e.preventDefault();
});



function startSlideShow(slideshowId) {
    let slideIndex = 0;
    const slides = document.querySelectorAll(`#${slideshowId} .slider`);
    let slideInterval;

    function showSlides() {
        for (let i = 0; i < slides.length; i++) {
            slides[i].style.display = "none"; // Hide all slides
        }
        slideIndex++;
        if (slideIndex > slides.length) {
            slideIndex = 1; // Reset to the first slide
        }
        slides[slideIndex - 1].style.display = "block"; // Show the current slide
    }

    function plusSlides(n) {
        slideIndex += n - 1; // Adjust the slide index
        clearInterval(slideInterval); // Stop the auto-rotation temporarily
        showSlides();
        startSlideShow(slideshowId); // Restart the auto-rotation
    }

    function initializeSlideShow() {
        slideInterval = setInterval(showSlides, 3000); // Rotate slides every 3 seconds
        showSlides(); // Show the first slide
    }

    // Start the slideshow
    initializeSlideShow();

    // Attach plusSlides function to buttons
    window.plusSlides = plusSlides;
}

// Initialize both slideshows
startSlideShow('slideshow1');
startSlideShow('slideshow2');

// JavaScript function to toggle the visibility of hidden content
function toggleContent() {
    const extraContent = document.getElementById('extraContent');
    const toggleButton = document.getElementById('toggleButton');

    if (extraContent.classList.contains('d-none')) {
        // Show additional content
        extraContent.classList.remove('d-none');
        toggleButton.textContent = 'Show Less';
    } else {
        // Hide the content
        extraContent.classList.add('d-none');
        toggleButton.textContent = 'Show More';
    }
}

const toggleButton = document.getElementById('toggleButton');
const passwordInput = document.getElementById('password');

// Enable button only if password matches
passwordInput.addEventListener('input', function() {
    if (passwordInput.value === 'abhinandan@123#') {  // Replace 'yourpassword' with the desired password
        toggleButton.disabled = false; // Enable the button
    } else {
        toggleButton.disabled = true; // Disable the button
    }
});

// Toggle visibility of hidden links
+toggleButton.addEventListener('click', function() {
    const hiddenLinks = document.getElementById('hiddenLinks');
    if (hiddenLinks.style.display === 'none' || hiddenLinks.style.display === '') {
        hiddenLinks.style.display = 'block'; // Show the hidden section
        this.textContent = 'Hide Links'; // Change button text
    } else {
        hiddenLinks.style.display = 'none'; // Hide the section
        this.textContent = 'Show Links'; // Revert button text
    }
});

function openPDF(pdfFileName) {
    // Opens the PDF in a new browser tab or window
    window.open(`/uploads/${pdfFileName}`, '_blank');
}


// Function to display the alert with contact details
document.getElementById('movable-button').addEventListener('click', function() {
    alert('Contact Details:\nName: Abhinandan H.S School\nEmail: \nPhone: ');
});