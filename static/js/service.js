"use strict";

service = {
    

    base: function (url, data = {}) {

        axios.post(url, data).then( response => {

        })
    },

    update: function (todo, status, ) {

        const { endpoint : url, taskId : id, method : _method } = todo.dataset

        if(url && id && status) {

            this.base(url, { id, status, _method })
        }
    },

}