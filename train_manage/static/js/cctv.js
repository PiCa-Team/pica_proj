function zoomVideo(video) {
    if (!video.classList.contains('video-zoomed')) {
        // 다른 비디오의 확대를 중지하고 중앙에 위치시킵니다.
        const videos = document.querySelectorAll('.video-container video');
        videos.forEach((v) => {
            if (v !== video) {
                v.classList.remove('video-zoomed');
            }
        });

        video.classList.add('video-zoomed');
    } else {
        video.classList.remove('video-zoomed');
    }
}