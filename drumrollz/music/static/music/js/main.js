var AlbumsListPage = {
    init: function(){
        this.$container = $('.albums-container');
        this.render();
        this.bindEvents();
    },

    render: function(){

    }
};

var SongListPage = {
    init: function(){
        this.$container = $('.songs-container');
        this.render();
        this.bindEvents();
    },

    render: function(){

    },

};

$(document).ready(function(){
    AlbumsListPage.init();
    SongListPage.init();
});