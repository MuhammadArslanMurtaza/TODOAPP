/**
 * App Class 
 *
 * @author		Carl Victor Fontanos
 * @author_url	www.carlofontanos.com
 *
 */

/**
 * Setup a App namespace to prevent JS conflicts.
 */
var app = {
	
	Todo: function() {
		this.init = function() {
			this.update_todo();
			this.create_todo();
		}
		
		this.update_todo = function(){
			$('.update-todo').ajaxForm({
				beforeSerialize: function() {
					update_ckeditor_instances();
					wave_box('on');
				},
				success: function(response, textStatus, xhr, form) {
					
					if(response.status == 0){
						Lobibox.notify('error', {msg: response.message, size: 'mini', sound: false});
					}
					
					if(response.status == 1){
						Lobibox.notify('success', {msg: response.message, size: 'mini', sound: false});
					}
					
					wave_box('off');
				}
            });
		}
		
		this.create_todo = function(){
			$('#createt_odo').ajaxForm({
				beforeSerialize: function() {
					update_ckeditor_instances();
					wave_box('on');
				},
				success: function(response, textStatus, xhr, form) {
					
					if(response.status == 0){
						Lobibox.notify('error', {msg: response.message, size: 'mini', sound: false});
					}
					
					if(response.status == 1){
						Lobibox.notify('success', {msg: response.message, size: 'mini', sound: false});
						setTimeout(function(){
							window.location.href = module_path + 'user/alltodolist/'
						}, 3000);
					}
					
					wave_box('off');
				}
            });
		}
	},

	User: function() {
		this.init = function() {
			this.update_account();
			this.create_account();
		}
		
		this.update_account = function(){
			$('.update-account').ajaxForm({
				beforeSerialize: function() {
					update_ckeditor_instances();
					wave_box('on');
				},
				success: function(response, textStatus, xhr, form) {
					
					if(response.status == 0){
						Lobibox.notify('error', {msg: response.message, size: 'mini', sound: false});
					}
					
					if(response.status == 1){
						Lobibox.notify('success', {msg: response.message, size: 'mini', sound: false});
					}
					
					wave_box('off');
				}
            });
		}
		
		this.create_account = function(){
			$('.create-account').ajaxForm({
				beforeSerialize: function() {
					update_ckeditor_instances();
					wave_box('on');
				},
				success: function(response, textStatus, xhr, form) {
					
					if(response.status == 0){
						Lobibox.notify('error', {msg: response.message, size: 'mini', sound: false});
					}
					
					if(response.status == 1){
						Lobibox.notify('success', {msg: response.message, size: 'mini', sound: false});
						setTimeout(function(){
							window.location.href = module_path + 'user/account/'
						}, 3000);
					}
					
					wave_box('off');
				}
            });
		}
	},
	
	/**
     * Global
     */
    Global: function () {
		
		/**
		 * This method contains the list of functions that needs to be loaded
		 * when the "Global" object is instantiated.
		 *
		 */
		this.init = function() {
			this.set_ckeditor();
		}
		
		/**
		 * Load CKEditor plugin
		 */
		this.set_ckeditor = function() {
			if($('#ck-editor-area').length){
				load_ckeditor('ck-editor-area', 300);
			}
		}
	}
}

/**
 * When the document has been loaded...
 *
 */
jQuery(document).ready( function () {
		
	global = new app.Global(); /* Instantiate the Global Class */
	global.init(); /* Load Global class methods */
	
	todos = new app.Todo(); /* Instantiate the todos Class */
	todos.init(); /* Load todos class methods */
	
	user = new app.User(); /* Instantiate the User Class */
	user.init(); /* Load User class methods */
	
});