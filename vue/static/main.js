//自定义弹框
function Toast(msg,duration){
    duration=isNaN(duration)?3000:duration;
    var m = document.createElement('div');
    m.innerHTML = msg;
    m.style.cssText="width: 60%;min-width: 150px;opacity: 0.7;height: 40px;color: rgb(255, 255, 255);line-height: 40px;text-align: center;border-radius: 5px;position: fixed;top: 40%;left: 20%;z-index: 999999;background: rgb(0, 0, 0);font-size: 13px;font-family: Arial, Helvetica, sans-serif;";
    document.body.appendChild(m);
    setTimeout(function() {
        var d = 0.5;
        m.style.webkitTransition = '-webkit-transform ' + d + 's ease-in, opacity ' + d + 's ease-in';
        m.style.opacity = '0';
        setTimeout(function() { document.body.removeChild(m) }, d * 1000);
    }, duration);
}


Vue.component("listpage", {
    template: `
    <div>
        <h5>{{block_title}}</h5>
        {{ _updateView }}
        <div id="listpage_ul">
            <input id="input_area" v-model="to_add" :placeholder="to_add_palceholder"></input>
            <button @click="addRecv(to_add)">新增</button>
            <button @click="testSend()" v-show="testButtonShow">发送测试</button>
            <tr id="listpage_li" v-for="(recv_value, recv_key, index) in recvivers" >
                <td><span>{{ recv_key }}</span></td>
                <td><input type="checkbox" id="checkbox" :checked="recv_value.is_recv" @click="updateRecv(recv_key, $event.target.checked)"></td>
                <td><button @click="deleteRecv(recv_key)">删除</button></td>
            </tr>
        </div>
    </div>
    `,
    data() {
        return {
            "to_add": "",
            "recvivers": "",
        }
    },
    props: {
        api_url: String,
        to_add_palceholder: String,
        block_title: String
    },
    mounted() {
        this.updateView()
    },
    methods: {
        addRecv(to_add) {
            if (to_add) {
                var form = new FormData();
                form.append('account', to_add);
                axios.post(this.api_url, form).then(response => (
                    console.log(this.recvivers),
                    this.$set(this.recvivers, to_add, { "is_recv": 1 }),
                    Toast(response.data.msg)
                )).catch(function (err) {
                    console.log(err)
                })
            }
        },
        updateRecv(account, is_recv) {
            is_recv = is_recv ? 1 : 0;
            var form = new FormData();
            form.append('account', account);
            form.append('is_recv', is_recv);
            axios.put(this.api_url, form).then(response => (
                // console.log(this.mail_recvivers),
                console.log(account, is_recv)
            )).catch(function (err) {
                console.log(err)
            })
        },
        deleteRecv(account, index) {
            axios.delete(this.api_url + '?account=' + account).then(response => (
                Vue.delete(this.recvivers, account)
            )).catch(function (err) {
                console.log(err)
            })
        },
        updateView() {
            // 加载收件人列表
            axios.get(this.api_url).then(response => (
                this.recvivers = response.data
            )).catch(function (err) {
                console.log(err)
            })
        },
        testSend() {
            // 加载收件人列表
            axios.get('/notice/test/' + this.api_url.split('/').pop()).then(response => (
                Toast(response.data.msg)
            )).catch(function (err) {
                console.log(err)
            })
        }
    },
    computed: {
        _updateView() {
            return this.updateView()
        },
        testButtonShow(){
            return this.api_url.split('/').pop() != 'allowed_sec_keys'
        }
    }
})


var main = new Vue({
    el: "#main",
    data: {
        "send_mail_account": "",
        "send_mail_password": "",
        "b64raw": "",
        "is_show_map": {
            'mail_block': true,
            'serverchan_block': false,
            'sec_keys_block': false,
        }
    },
    mounted() {
        // 邮箱配置
        axios.get('/send/mail_backend').then(response => (
            this.send_mail_account = response.data.account,
            this.send_mail_password = response.data.password
        )).catch(function (err) {
            console.log(err)
        })

    },
    methods: {
        updateSendMail() {
            var form = new FormData();
            form.append('account', this.send_mail_account);
            form.append('password', this.send_mail_password);
            axios.post('/send/mail_backend', form).then(response => (
                Toast(response.data.msg)
            )).catch(function (err) {
                console.log(err)
            })
        },
        clickTab(block_name) {
            // 点击tab，用于切换
            for (var key in this.is_show_map) {
                if (key === block_name) {
                    this.is_show_map[key] = !Boolean(this.is_show_map[key])
                } else {
                    this.is_show_map[key] = false
                }
            }
        },
        tabIsShow(block_name) {
            // 是否展示当前tab，用于切换
            return Boolean(this.is_show_map[block_name])
        }
    },
    computed: {
        b64encodeValue() {
            return window.btoa(this.b64raw)
        },

    }
})


