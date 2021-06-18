let v = new Vue({
    el: "#app",
    data: {
        password: "",
        errorPassword: ""
    },
    methods: {
        checkPassword(e){
            
            this.password = e.target.value;
            if(this.password.length < 8){
                this.errorPassword = "Пароль меньше 8 символов";
                console.log(this.errorPassword);
            }
        }
    },
    computed: {
        getPassword(){
            console.log(this.password);
            return this.password;
        }
    }
});