
// function get_site_from_url() {
//     arr = window.location.href.split('#')
//     site = ''
//     if (arr.length === 2) {
//         site = arr.pop()
//     }
//     return site
// }

// var default_site = get_site_from_url()


// Vue.component("listpage", {
//     template: `
//     <table v-show="isShow">
//     listpage
//     {{ query_site }} 站点信息
//     {{ query_site }}
//     {{ get_cookies }}  <!-- 更改数据 -->
//     {{ total }}
//     <tr>
//         <td v-for="col in col_list">{{ col }}</td>
//     </tr>

//     <tr v-for="(item, index) in list_data">
//         <td> {{ item.cookies_name }} </td>
//         <input :value="item.cookies"  v-model="input_cookies"></input>
//         <td> {{ item.modified }} </td>
//         <td v-text="item.status?'不可用':'可用'"></td>
//         <td :key="item.no">修改</td>
//         <td :key="item.no" @click="deleteCookies(item.id, index)">删除</td>
//     </tr>

// </table>`,
//     data() {
//         return {
//             "list_data": "",
//             "input_cookies": "",
//             "current_editing_cookies": "",
//             "col_list": ["Name", "Cookie", "ModifiedAt", "Status"],
//             "total": "",
//         }
//     },
//     props: ["query_site"],
//     computed: {
//         get_cookies() {
//             if (this.query_site != '') {
//                 axios.get('/cookies_all?site=' + this.query_site).then(response => (
//                     this.list_data = response.data.cookies,
//                     this.total = response.data.total
//                 )).catch(function (err) {
//                     console.log(err)
//                 })
//             }
//         },
//         isShow() {
//             return this.query_site != ''
//         }
//     },
//     methods: {
//         deleteCookies(cookies_id, index) {
//             axios.delete('/cookies?cookies_id=' + cookies_id).then(
//                 response => (this.list_data.splice(index, 1))
//             ).catch(response => (''))
//         },
//         clickToEdite(cookies){
//             this.current_editing_cookies =  cookies
//             console.log(cookies)
//         }
//     }

// })


var main = new Vue({
    el: "#main",
    data: {
        "send_mail_account": "",
        "send_mail_password": "",
        "b64raw": "",
        "to_add_mail": "",
        "mail_recvivers": new Array(),
    },
    mounted() {
        // 邮箱配置
        axios.get('/mail/send').then(response => (
            this.send_mail_account = response.data.account,
            this.send_mail_password = response.data.password
        )).catch(function (err) {
            console.log(err)
        });
        // 邮箱收件人列表
        axios.get('/mail/recv').then(response => (
            this.mail_recvivers = response.data
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
        addRecvMail(account) {
            if (account) {
                var form = new FormData();
                form.append('account', account);
                axios.post('/mail/recv', form).then(response => (
                    console.log(this.mail_recvivers),
                    this.$set(this.mail_recvivers, account, { "is_recv": 1 }),
                    alert(response.data.msg)
                )).catch(function (err) {
                    console.log(err)
                })
            }
        },
        updateRecvMail(account, is_recv) {
            is_recv = is_recv ? 1 : 0;
            var form = new FormData();
            form.append('account', account);
            form.append('is_recv', is_recv);
            axios.put('/mail/recv', form).then(response => (
                // console.log(this.mail_recvivers),
                console.log(account, is_recv)
            )).catch(function (err) {
                console.log(err)
            })
        },
        deleteSendMail(account, index) {
            axios.delete('/mail/recv?account=' + account).then(response => (
                Vue.delete(this.mail_recvivers, account)
            )).catch(function (err) {
                console.log(err)
            })
        }
    },
    computed: {
        b64encodeValue() {
            return window.btoa(this.b64raw)
        }
    }
})


