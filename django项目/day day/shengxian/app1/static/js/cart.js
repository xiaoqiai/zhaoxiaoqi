$(function () {
    // 计算小计
    function total(el) {
        $('.subtotal').each(function (i, el) {
            // 先找到父级别标签 cart_list_td
            let parent = $(el).parents('.cart_list_td');
            // 找到数量
            let num = parent.find('.num_show').val();
            // 找到单价，给价格乘以100，变成整数，避免小数运算出现误差
            let price = parent.find('.price').html() * 100;
            // 计算小计，前面乘以100，这里要再除以100
            $(el).html((num * price / 100).toFixed(2));
        });
    }

    // 计算总金额
    function amount() {
        let sum = 0, count = 0;
        // 获取所有选中的商品的复选框元素的父级的 ul 标签
        let parent = $('.select:checked').parents('.cart_list_td');
        parent.find('.subtotal').each(function (i, el) {
            sum += $(el).html() * 100
        });
        parent.find('.num_show').each(function (i, el) {
            count += parseInt($(el).val())
        });
        $('#sum').html((sum / 100).toFixed(2));
        $('#count').html(count)
    }

    function calc() {
        total(); // 加载页面初始化计算小计
        amount();
    }

    calc();

    // 异步请求修改数量
    function update_number(goods_id, number) {
        $.ajax({
            url: '/update_cart_number/' + goods_id + '/' + number + '/',
            type: 'post',
            headers: {'X-CSRFTOKEN': $.cookie('csrftoken')},
            complete: function () {
                location.reload()
            }
        });
    }

    // 增加数量
    $('.add').click(function () {
        $(this).next().val(function (i, v) {
            let number = parseInt(v) + 1;
            update_number($(this).attr('data-id'), number);
            return number;
        });
        calc();
    });
    // 减少数量
    $('.minus').click(function () {
        $(this).prev().val(function (i, v) {
            let number = parseInt(v);
            if (v > 1) {
                number -= 1
            }
            update_number($(this).attr('data-id'), number);
            return v;
        });
        calc();
    });

    $('.num_show').focus(function () {
        $(this).attr('preValue', $(this).val())
    });
    $('.num_show').change(function () {
        if (!/^\d+$/.test($(this).val())) {
            $(this).val($(this).attr('preValue'))
        } else {
            update_number($(this).attr('data-id'), $(this).val());
        }
    });

    // 点击选中某个商品
    $('.select').change(calc);
    // 全选
    $('#selectAll').change(function () {
        $('.select').each(function (i, el) {
            el.checked = $('#selectAll').get(0).checked
        });
        calc();
    });

    // 点击结算按钮进行结算请求
    $('#jiesuan').click(function () {
        let data = [];
        $('.select:checked').parents('.cart_list_td').find('.num_show').each(function (i, el) {
            data.push($(el).attr('data-id'));
        });
        $(this).attr('href', '/place_order/?ids=' + JSON.stringify(data));
    })
});