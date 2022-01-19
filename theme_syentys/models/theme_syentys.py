from odoo import models


class ThemeSyentys(models.AbstractModel):
    _inherit = 'theme.utils'

    def _theme_syentys_post_copy(self, mod):
        self.enable_asset('website.ripple_effect_scss')
        self.enable_asset('website.ripple_effect_js')
        self.enable_view('website.template_footer_centered')
        self.enable_header_off_canvas()