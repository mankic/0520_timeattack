function upload() {
    let file = $('#upload-file')[0].files[0]    // id:uplad-file, 해당 파일 지정해주는 형식
    let title = $('#upload-title').val()
    let form_data = new FormData()  // 파일 보낼때는 new FormData()를 사용해서 담아보내준다.

    form_data.append("file_give", file)     // .append를 사용해 " "안의 이름으로 file 변수를 넣는다.
    form_data.append("title_give", title)

    $.ajax({
        type: "POST",
        url: "/upload",
        data: form_data,    // FormData
        cache: false,
        contentType: false,
        processData: false,
        success: function (response) {
            alert(response["result"])
        }
    });
  }

  function search() {
    let title = $('#search-title').val()
    let form_data = new FormData()

    form_data.append("title_give", title)

    $.ajax({
        type: "POST",
        url: "/search",
        data: form_data,
        cache: false,
        contentType: false,
        processData: false,
        success: function (response) {
            let predictions = response["predictions"]
            $('.result').remove()
            for (let i = 0; i < predictions.length; i++) {
                let path = predictions[i]['path']
                let result = predictions[i]['result']

                // 응답받은값 이미지와 결과 가져오기
                let temp_html = `<div class="result"><img src="${path}" width="100px"/>
                                <p>${result}</p></div>`
                $('.search').append(temp_html)
            }
        }
    });
  }

  function preview() {
    let frame = document.getElementById('frame');
    frame.src=URL.createObjectURL(event.target.files[0]);
    frame.style.display = 'block';
  }