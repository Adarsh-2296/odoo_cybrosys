/** @odoo-module */
import { renderToElement } from "@web/core/utils/render";
import publicWidget from "@web/legacy/js/public/public_widget";
import { rpc } from "@web/core/network/rpc";

publicWidget.registry.get_product_tab = publicWidget.Widget.extend({
   selector : '.dynamic_snippet_blog',
   async willStart() {
       let result = await rpc('/get_machine', {});
       var a = [1,2,3,4,5,6]
       let a1 = a.splice(0, 2);
       console.log(a1)
       let a2 = a.splice(0, 2);
       console.log(a2)
       let a3 = a.splice(0, 2);
       console.log(a3)
       let a4 = a.splice(0, 2);
       console.log(a4)
       console.log(result['machine'])
       var chunks = result['machine'].splice(0,4);
        	chunks[0].is_active = true
        	this.$el.find('#courosel').html(
            	this.$target.empty().html(renderToElement('machine_management.dynamic_filter_template_machine', {result: chunks}))
        	)
       // if(result){
       //     this.$target.empty().html(renderToElement('machine_management.dynamic_filter_template_machine', {result: result}))
       // }

   },
});

// odoo.define('machine_management.snippet', function(require) {
// 	'use strict';
// 	var PublicWidget = require('web.public.widget');
// 	var rpc = require('web.rpc');
// 	var core = require('web.core');
// 	var qweb = core.qweb;
// 	var Dynamic = PublicWidget.Widget.extend({
//     	selector: '.dynamic_snippet_blog',
//     	willStart: async function() {
//         	var self = this;
//         	await rpc.query({
//             	route: '/get_machine',
//         	}).then((data) => {
//             	this.data = data;
//         	});
//     	},
//     	start: function() {
//         	var chunks = _.chunk(this.data, 4)
//         	chunks[0].is_active = true
//         	this.$el.find('#courosel').html(
//             	qweb.render('machine_management.machine_snippet', {
//                 	chunks
//             	})
//         	)
//     	},
// 	});
// 	PublicWidget.registry.dynamic_snippet_blog = Dynamic;
// 	return Dynamic;
// });
