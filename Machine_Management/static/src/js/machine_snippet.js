/** @odoo-module */
import { renderToFragment } from "@web/core/utils/render";
import publicWidget from "@web/legacy/js/public/public_widget";
import { rpc } from "@web/core/network/rpc";

publicWidget.registry.get_product_tab = publicWidget.Widget.extend({
   selector : '.dynamic_snippet_blog',
   async willStart() {
       let result = await rpc('/get_machine', {});
       let chunks =[]
       const date = new Date();
       let ms = date.getUTCMilliseconds();
       let length = Math.ceil(result['machine'].length/4)
       for(let i=0; i<length;i++){
            chunks.push(result['machine'].splice(0,4));
       }
        	chunks[0].is_active = true
       if(chunks){
       this.$el.find('#courosel').html(
            renderToFragment('machine_management.dynamic_filter_template_machine', {
                result: chunks,
                id : ms
            })
        );
        	}
   },
});

