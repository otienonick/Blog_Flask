function like(postId){
    const likeCount = document.getElementById(`likes-count-${postId}`);

    fetch(`/like-post/ ${postId}`,{method : 'POST'}).then((res) => res.json()).then((data) => {
        likeCount.innerHTML = data['likes'];
    });

}