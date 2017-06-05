/**
 * 引入CSS样式
 */
(function (){
      var paths  = [
            "/static/mkeditor/codemirror/lib/codemirror.css",
            "/static/mkeditor/themes/base16-light.css",
            "/static/mkeditor/themes/default.css",
            "/static/mkeditor/bootstrap/dist/css/bootstrap.min.css",
            "/static/mkeditor/font/iconfont.css",
            "/static/mkeditor/themes/editor.css",
      ],
      baseURL = '';
      for (var i=0,pi;pi = paths[i++];) {
            var link = document.createElement("link");
            link.type = "text/css";
            link.rel = "stylesheet";
            link.href = baseURL + pi;
            document.getElementsByTagName("head")[0].appendChild(link);
      }
})();
