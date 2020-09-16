
// //////////////  更改秘密  /////////////////

var mopwd;
var newpwd;


function showModifyLayer() {
    let index = layer.open({
        type: 1,
        btn: ['取消', '确定'],
        title: "修改密码",
        area: ["660px", "320px"],
        content: $("#modifypwdlayer"),
        //++enter
        success: function (layero, index) {
            $(document).on('keydown', function (e) {
                if (e.keyCode == 13) {
                    deleteFile(index);
                }
            });
            getModifyPwd()

        },
        cancel: function (index, layero) {
            $("#mopwd").val("")
            $("#mopwd-aux").css("display", "none")
            $("#newpwd1").val("")
            $("#newpwd1-aux").css("display", "none")
            $("#newpwd2").val("")
            $("#newpwd2-aux").css("display", "none")
        },
        yes: function (index) {
            layer.close(index);
        }, btn2: function (index) {

            confirmModifyPwd(index)
            // return false
        }
    });
}

function getModifyPwd() {
    var pwd
    $("#mopwd").blur(function () {
        mopwd = $("#mopwd").val().trim();
        if (mopwd.length == 0) {
            $("#mopwd-aux").css({
                display: "block",
                color: "#ff1010",
            }).html("请输入原密码")
        }
        // else {
        //     //发送ajax获得原密码 pwd
        //     pwd = 1

        //     if (mopwd != pwd) {
        //         $("#mopwd-aux").css({
        //             display: "block",
        //             color: "#ff1010",
        //         }).html("密码不正确")
        //     } else {
        //         $("#mopwd-aux").css({
        //             display: "block",
        //             color: "#5FB878"
        //         }).html("输入正确")
        //     }
        // }
    });

    let newpwd1 = $("#newpwd1").val().trim()
    $("#newpwd1").blur(function () {
        newpwd1 = $("#newpwd1").val().trim()
        if (newpwd1.length == 0) {
            $("#newpwd1-aux").css({
                display: "block",
                color: "#ff1010"
            }).html("请输入新密码")
        } else {
            $("#newpwd1-aux").css({
                display: "block",
                color: "#5FB878"
            }).html("输入正确")
        }
    })

    $("#newpwd2").focus(() => {
        let newpwd1 = $("#newpwd1").val().trim()
        if (newpwd1.length == 0) {
            $("#newpwd1-aux").css({
                display: "block",
                color: "#ff1010"
            }).html("请输入新密码")
        }
    })

    $("#newpwd2").blur(function () {
        let newpwd2 = $("#newpwd2").val().trim()
        if (newpwd2.length == 0) {
            $("#newpwd2-aux").css({
                display: "block",
                color: "#ff1010"
            }).html("请输入新密码")
        } else if (newpwd1 != newpwd2) {
            $("#newpwd2-aux").css({
                display: "block",
                color: "#ff1010"
            }).html("两次输入不一致")
            $("#newpwd1-aux").css({
                display: "block",
                color: "#ff1010"
            }).html("两次输入不一致")

        } else if (newpwd1 == newpwd2 && newpwd1 == pwd) {
            $("#newpwd2-aux").css({
                display: "block",
                color: "#ff1010"
            }).html("新密码不能与原密码相同")
            $("#newpwd1-aux").css({
                display: "block",
                color: "#ff1010"
            }).html("新密码不能与原密码相同")
        } else {
            $("#newpwd1-aux").css({
                display: "block",
                color: "#5FB878"
            }).html("输入正确")
            $("#newpwd2-aux").css({
                display: "block",
                color: "#5FB878"
            }).html("输入正确")
            newpwd = newpwd1
            // $("#adduserlayer").data("new_pwd", newpwd1)
        }
    });
}

function confirmModifyPwd(index) {
    // let newpwd = $("#adduserlayer").data("new_pwd")
    //发送ajax
    var dat = JSON.stringify({ "old_password": mopwd, "new_password": newpwd });
    console.log(dat)


    $.ajax({
        type: "post",
        url: "/user/changePassword",
        async: false,
        data: dat,
        contentType: 'application/json',
        processData: false,
        error: function (request) {
            layer.alert('操作失败', {
                icon: 2,
                title: "提示"
            });
        },
        success: function (ret) {
            if (ret.errno == "0") {
                layer.alert('注册成功', {
                    icon: 2,
                    title: "提示",
                });
                layer.closeAll();
                window.location.href = "/";
                rel = "external nofollow";
            } else {
                layer.alert(ret.errmsg, {
                    icon: 2,
                    title: "提示",
                });
            }
        }
    })

    // $("#mopwd").val("")
    // $("#mopwd-aux").css("display", "none")
    // $("#newpwd1").val("")
    // $("#newpwd1-aux").css("display", "none")
    // $("#newpwd2").val("")
    // $("#newpwd2-aux").css("display", "none")
    // layer.close(index);
}

/////////////////////////////////////////////////