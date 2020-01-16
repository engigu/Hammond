
// function get_site_from_url() {
//     arr = window.location.href.split('#')
//     site = ''
//     if (arr.length === 2) {
//         site = arr.pop()
//     }
//     return site
// }

// var default_site = get_site_from_url()


Vue.component("listpage", {
    template: `
    <div>
        <h5>{{block_title}}</h5>
        <ul>
            <input v-model="to_add"></input>
            <button @click="addRecv(to_add)">新增收件人</button>
            <li v-for="(recv_value, recv_key, index) in recvivers" >
                <td><span>{{ recv_key }}</span></td>
                <td><input type="checkbox" id="checkbox" :checked="recv_value.is_recv" @click="updateRecv(recv_key, $event.target.checked)"></td>
                <td><button @click="deleteRecv(recv_key)">删除</button></td>
            </li>
        </ul>
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
        block_title: String
    },
    mounted() {
        // 加载收件人列表
        axios.get(this.api_url).then(response => (
            this.recvivers = response.data
        )).catch(function (err) {
            console.log(err)
        })
    },
    methods: {
        addRecv(to_add) {
            if (to_add) {
                var form = new FormData();
                form.append('account', to_add);
                axios.post(this.api_url, form).then(response => (
                    console.log(this.recvivers),
                    this.$set(this.recvivers, to_add, { "is_recv": 1 }),
                    alert(response.data.msg)
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
        }
    },
    mounted() {
        // 邮箱配置
        axios.get('/mail/send').then(response => (
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
            axios.post('/mail/send', form).then(response => (
                alert(response.data.msg)
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


