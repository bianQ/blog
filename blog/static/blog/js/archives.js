$(function(){
    $('div.widget.widget-archives span').click(function(){
        if ($(this).siblings('a').attr('value') === 'hide'){
            // 隐藏所有 a 标签
            $('div.widget.widget-archives ul li a').hide();
            // 将所有 a 标签的 value 改为 hide
            $('div.widget.widget-archives ul li a').attr('value', 'hide');
            // 显示被点击标签的同级 a 标签
            $(this).siblings('a').show();
            // 将被显示的 a 标签的 value 改为 show
            $(this).siblings('a').attr('value', 'show');
        }else if ($(this).siblings('a').attr('value') === 'show'){
            // 当被点击标签的同级 a 标签的 value 为show，则隐藏此标签，并将 value 改为 hide
            $('div.widget.widget-archives ul li a').hide();
            $(this).siblings('a').attr('value', 'hide');
        }
    })
})