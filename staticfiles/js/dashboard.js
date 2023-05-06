window.addEventListener('DOMContentLoaded', function() {
            var iframe = document.getElementById('superset-iframe');
            if (iframe) {
                iframe.onload = function() {
                    setTimeout(function() {
                        iframe.style.height = iframe.contentWindow.document.body.scrollHeight + 'px';
                    }, 100);
                };
            }
        });