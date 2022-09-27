// import "@/mock/index"

/**
 * 后端异步通信函数
 * @param {*} data 通信请求的内容
 * @param {*} url 请求的目标后端url
 * @param {*} method 请求方法('get'/'post')
 * @param {*} target_status 目标返回码谓词(返回true时接受)，默认接受2**
 * @param {*} timeout 超时限制(ms)
 * @param {*} resolve 成功返回后执行的回调，传入参数{code, data}
 * @param {*} reject 失败后执行的回调，默认控制台输出
 */
const request_json = (data, url, method, 
    resolve=(res) => {
        console.log(res)
    }, 
    reject=(err) => {
        console.log(err)
    },
    timeout=100000, 
    target_status=(n) => (200<=n && n<300), 
    ) => { 
    return new Promise(function(resolve, reject){
        var xhr = new XMLHttpRequest()
        xhr.onreadystatechange = function() {
            if(xhr.readyState === 4) {
                // console.log(xhr.responseText)
                var res
                try{
                    res = JSON.parse(xhr.responseText)
                }catch{
                    reject(xhr.responseText)
                    return
                }
                
                if(target_status(res['code'])) {
                    resolve(res)
                }
                else {
                    reject(res)
                }
            }
        }
        xhr.timeout = timeout
        if(method == 'GET' || method == 'get') {
            let param = Object.keys(data).map(function(key) {
                return encodeURIComponent(key) + '=' + encodeURIComponent(data[key]);
            }).join('&')
            url = url + '?' + param
        }
        // console.log(data)
        xhr.open(method, url, true)
        xhr.setRequestHeader('Cookie', document.cookie)
        xhr.setRequestHeader('Content-type', "application/json")
        xhr.send(JSON.stringify(data))
    }).then(resolve, reject)
}
export {request_json}