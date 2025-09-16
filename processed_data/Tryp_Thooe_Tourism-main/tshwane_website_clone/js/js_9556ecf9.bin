// -------------------------------------------------------------------------------------------
// Tab Section and Slideshow Section
// =================================
//
// @since 5.0		extended to support slideshow section
// -------------------------------------------------------------------------------------------
(function($)
{
	"use strict";

	$.fn.avia_sc_tab_section = function()
	{
		var win 			= $(window),
			browserPrefix 	= $.avia_utilities.supports('transition'),
			cssActive 		= this.browserPrefix !== false ? true : false,
			isMobile 		= $.avia_utilities.isMobile,
			isTouchDevice	= $.avia_utilities.isTouchDevice,
			mobile_no_animation = $( 'body' ).hasClass( 'avia-mobile-no-animations' ),
			transform3d		= document.documentElement.className.indexOf('avia_transform3d') !== -1 ? true : false,
			transition		= {},
			animations = [
							'avia_animate_when_visible',
							'avia_animate_when_almost_visible',
							'av-animated-generic',
							'av-animated-when-visible',
							'av-animated-when-almost-visible',
							'av-animated-when-visible-95'
						];

		return this.each( function()
		{
			var container 		= $(this),
				tabs			= container.find('.av-section-tab-title'),
				tab_outer		= container.find('.av-tab-section-outer-container'),
				tab_wrap		= container.find('.av-tab-section-tab-title-container'),
				tab_nav			= container.find('.av_tab_navigation'),		//	dummy structure used for sliding logic
				arrows_wrap		= container.find('.av-tabsection-arrow'),	//	arrows to scroll tab buttons
				arrows			= arrows_wrap.find('.av-tab-section-slide'),
				slides_wrap		= container.find('.av-slide-section-container-wrap'),
				slide_arrows_wrap = container.find('.av-tabsection-slides-arrow'),	//	arrows to scroll slides
				slide_arrows	= slide_arrows_wrap.find('.av-tab-section-slide-content'),
				slide_dots_wrap = container.find('.av-tabsection-slides-dots'),		//	dots to scroll slides
				slide_dots		= slide_dots_wrap.find('.goto-slide'),
				content_wrap	= container.find('.av-tab-section-inner-container'),
				single_tabs		= container.find('.av-animation-delay-container'), //for elements inside the tab that receive waypoint animation
				layout_tab_wrap = container.find('.av-layout-tab'),
				inner_content	= container.find('.av-layout-tab-inner'),
				flexible    	= container.is('.av-tab-content-auto'),
				minimumBrowserHeight = container.hasClass( 'av-minimum-height'),
				current_content = null,		// container.find('.__av_init_open') => .av-layout-tab,
				current_tab_id  = '1',		// current_content.data( 'av-tab-section-content' ),
				current_iTab_id = 1,		// 'undefined' != typeof current_tab_id ? parseInt( current_tab_id, 10 ) : 1,
				min_width		= 0,
				transition_action = 'none',
				slideshowOptions = {
								animation: 'av-tab-slide-transition',
								autoplay: false,
								loop_autoplay: 'once',			//	'endless' | 'once'
								interval: 5,
								loop_manual: 'manual-endless',	//	'manual-endless' | 'manual-once'
								autoplay_stopper: false,
								noNavigation: false
							},
				slideshowData = tab_outer.data( 'slideshow-data' ),		//	returns decoded json object
				deepLinksToTabs = {},				//	deeplink: tabID  allows case insensitive retrieve of hash tag
				timeoutIDAutoplay = null;

			if( 'undefined' != typeof slideshowData )
			{
				slideshowOptions = $.extend( {}, slideshowOptions, slideshowData );
			}

			layout_tab_wrap.each( function ()
			{
				var tab = $( this ),
					link = tab.data( 'av-deeplink-tabs' ),
					id = tab.data( 'av-tab-section-content' );

				if( link )
				{
					deepLinksToTabs[ link.toLowerCase() ] = id;
				}
			});

			//	__av_init_open might not set because we cannot check for invalid initial open slide number in php - we set it here
			current_tab_id = container.find( '.av-active-tab-title' ).data( 'av-tab-section-title' );
			current_tab_id = 'undefined' != typeof current_tab_id ? current_tab_id : '1';
			current_iTab_id = parseInt( current_tab_id, 10 );
			current_content = container.find( '[data-av-tab-section-content="' + current_tab_id + '"]' );
			current_content.addClass( '__av_init_open av-active-tab-content' );

			if( 'av-tab-slide-transition' == slideshowOptions.animation )
			{
				transition_action = 'slide_sidewards';
			}
			else if( 'av-tab-slide-up-transition' == slideshowOptions.animation )
			{
				transition_action = 'slide_up';
			}
			else if( 'av-tab-fade-transition' == slideshowOptions.animation )
			{
				transition_action = 'fade';
			}

			//	due to translate animations are not working correctly with waypoint script we have to add this here
			if( 'slide_up' == transition_action )
			{
				$.each( animations, function( index, value )
				{
					inner_content.find( '.' + value ).addClass( 'avia_start_animation_when_active' );
				});
			}

			var change_tab = function( e, prevent_hash )
				{
					e.preventDefault();

					//	ignore user click on tab buttons when slideshow
					if( container.hasClass( 'av-is-slideshow' ) && e.originalEvent !== undefined )
					{
						return;
					}

					var current_tab = $( e.currentTarget ),
//						current_arrow = current_tab.find('.av-tab-arrow-container span'),
						tab_nr = current_tab.data('av-tab-section-title'),
						iTab_nr = parseInt( tab_nr, 10 ),
						prev_content = current_content;

					tabs.removeClass( 'av-active-tab-title' );
					prev_content.removeClass( 'av-active-tab-content' );

					//	needed to avoid scroll on pageload when multiple tab sections on page
					current_tab.removeClass( 'no-scroll' );

					//	reset global scope !!
					current_content = container.find( '[data-av-tab-section-content="' + tab_nr + '"]' );
					current_tab_id = tab_nr;
					current_iTab_id = iTab_nr;

					current_tab.addClass( 'av-active-tab-title' );
					current_content.addClass( 'av-active-tab-content' );

					var new_pos = ( ( iTab_nr - 1 ) * -100 );

					if( $('body').hasClass('rtl') )
					{
						new_pos = ( ( iTab_nr - 1 ) * 100 );
					}

					//	set height of section depending on current content
					set_slide_height();

					if( ['none', 'slide_sidewards'].indexOf( transition_action ) >= 0 )
					{
						//	default tab section slide behaviour
						if( cssActive )
						{
							//move the slides
							new_pos = new_pos / tabs.length;
							transition['transform'] = transform3d ? "translate3d(" + new_pos  + "%, 0, 0)" : "translate(" + new_pos + "%,0)"; //3d or 2d transform?
							transition['left'] = "0%";
							content_wrap.css( transition );
						}
						else
						{
							content_wrap.css( 'left', new_pos + "%" );
						}
					}
					else if( 'slide_up' == transition_action )
					{
						layout_tab_wrap.css( 'opacity', 1 );

						//	default tab section slide behaviour
						if( cssActive )
						{
							var top = current_content.data( 'slide-top' );

							if( 'undefined' == typeof top )
							{
								top = 0;
							}

							//move the slides
							transition['transform'] = transform3d ? "translate3d(0, -" + top + "px, 0)" : "translate(0, -" + top + "px ,0)"; //3d or 2d transform?
							transition['left'] = "0";
							content_wrap.css( transition );
						}
						else
						{
							content_wrap.css( 'top', '-' + new_pos + 'px' );
						}

						layout_tab_wrap.filter(':not(.av-active-tab-content)').css( 'opacity', 0 );
					}

					set_tab_title_pos();
					set_slide_arrows_visibility( iTab_nr );
					set_slide_dots_visibility( iTab_nr );

					if( ! ( prevent_hash || slideshowOptions.autoplay ) )
					{
						var newHash = current_tab.attr( 'href' ),
							deepLink = current_content.data( 'av-deeplink-tabs' );

						if( 'undefined' != typeof( deepLink ) && '' != deepLink )
						{
							newHash = deepLink;
						}

						location.hash = newHash;
					}

					setTimeout( function()
					{
						current_content.trigger( 'avia_start_animation_if_current_slide_is_active' );

						//	fixes bug that animations do not work due to fn.avia_waypoints()
						if( ! isMobile || ( isMobile && ! mobile_no_animation ) )
						{
							single_tabs.not( current_content ).trigger( 'avia_remove_animation' );
						}
					}, 600 );
				},

				set_min_width = function()
				{
					min_width = 0;
					tabs.each( function()
					{
						min_width += $(this).outerWidth();
					});

					tab_wrap.css( 'min-width', min_width );
				},

				set_slide_height = function()
				{
					var tab_wrap_height = container.hasClass( 'av-hide-tabs' ) ? 0 : tab_wrap.height(),
						tab_wrap_add = tab_wrap_height ? tab_wrap.outerHeight() : 0,
						min_el_height = 0,
						cell_padding = 0,
						same_slide_height = 0,
						same_table_cell_height = 0,
						calc_el_height = 0;

					if( minimumBrowserHeight )
					{
						var css_height = container.hasClass( 'av-minimum-height-custom' ) ? container.data( 'av_minimum_height_px' ) : container.css( 'min-height' );
						css_height = parseInt( css_height, 10 );
						if( ! isNaN( css_height ) )
						{
							min_el_height = css_height;
						}

						if( ! min_el_height )
						{
							minimumBrowserHeight = false;
						}
					}

					if( ! flexible )
					{
						//	reset all slide content to actual height
						inner_content.css( 'height', '' );
						content_wrap.css( 'min-height', '' );

						var first = layout_tab_wrap.first();

						cell_padding = first.outerHeight() - first.height();

						layout_tab_wrap.each( function()
						{
							var content = $( this ),
								inner = content.find( '.av-layout-tab-inner' );

							same_slide_height = Math.max( same_slide_height, inner.height() );
						});

						same_table_cell_height = same_slide_height + cell_padding;
						calc_el_height = same_table_cell_height + tab_wrap_add;

						if( minimumBrowserHeight )
						{
							if( calc_el_height < min_el_height )
							{
								same_table_cell_height = min_el_height - tab_wrap_add;
								calc_el_height = min_el_height;
							}
						}

//						inner_content.height( same_table_cell_height );
						content_wrap.css( 'min-height', same_table_cell_height );
						content_wrap.css( 'height', same_table_cell_height );
					}
					else if( flexible && minimumBrowserHeight )
					{
						same_table_cell_height = min_el_height - tab_wrap_add;
						calc_el_height = min_el_height;

						content_wrap.css( 'min-height', same_table_cell_height );
						content_wrap.css( 'height', same_table_cell_height );
					}

					if( ['none', 'slide_sidewards', 'fade'].indexOf( transition_action ) >= 0 )
					{
						if( ! current_content.length )
						{
							return;
						}

						//	table and table cell - only needs to be adjusted when content adjusted to content height
						if( flexible )
						{
//							var old_height = inner_content.height();
							inner_content.height( 'auto' );

							//	since 4.8.9 changed to outerHeight because huge_padding is broken - padding is ignored
							var content_height = current_content.find( '.av-layout-tab-inner' ).height(),
								height = current_content.outerHeight(),
								outer_height = height + tab_wrap_height + 100;

							tab_outer.css( 'max-height', outer_height );
//							inner_content.height( old_height );
							inner_content.height( content_height );
							inner_content.css( 'overflow', 'hidden' );
						}

						setTimeout( function() { win.trigger( 'av-height-change' ); }, 600 );

						return;
					}

					//	'slide_up'
					var top = 0;

					layout_tab_wrap.each( function()
					{
						var content = $( this ),
							inner = content.find( '.av-layout-tab-inner' ),
							layout_tab_nr = content.data( 'av-tab-section-content' ),
							layout_iTab_nr = parseInt( layout_tab_nr, 10 ),
							outerHeight = content.outerHeight();

						content.data( 'slide-top', top );
						top += outerHeight;

						if( flexible && layout_iTab_nr == current_iTab_id )
						{
							//	adjust height of section to visible element
							tab_outer.css( 'max-height', outerHeight + tab_wrap_add );
							inner.css( 'overflow', 'hidden' );
						}
					});
				},

				set_tab_title_pos = function()
				{
					//	scroll the tabs if there is not enough room to display them all - rtl allign right to left !!
					var current_tab = container.find('.av-active-tab-title'),
						viewport = container.width(),
						left_pos = ( current_tab.position().left * - 1 ) - ( current_tab.outerWidth() / 2 ) + ( viewport / 2 );

					if( ! $('body').hasClass('rtl') )
					{
						if( viewport >= min_width )
						{
							left_pos = 0;
						}

						if( left_pos + min_width < viewport )
						{
							left_pos = ( min_width - viewport ) * -1;
						}

						if( left_pos > 0 )
						{
							left_pos = 0;
						}

						tab_wrap.css( 'left', left_pos );

						var show_prev = left_pos !== 0;
						var show_next = left_pos + min_width > viewport;

						set_arrows_visibility( show_prev, show_next );
					}
					else
					{
						var right_pos = 0;

						if( viewport < min_width )
						{
							if( left_pos + min_width > viewport )
							{
								if( left_pos > 0 )
								{
									left_pos = 0;
								}

								right_pos = ( left_pos + min_width - viewport ) * -1;
							}
						}

						tab_wrap.css( 'left', 'auto' );
						tab_wrap.css( 'right', right_pos );

						var show_prev = right_pos + min_width > viewport;
						var show_next = right_pos !== 0;

						set_arrows_visibility( show_prev, show_next );
					}
				},

				set_arrows_visibility = function( show_prev, show_next )
				{
					if( show_prev )
					{
						arrows_wrap.addClass( 'av-visible-prev' );
					}
					else
					{
						arrows_wrap.removeClass( 'av-visible-prev' );
					}

					if( show_next )
					{
						arrows_wrap.addClass( 'av-visible-next' );
					}
					else
					{
						arrows_wrap.removeClass( 'av-visible-next' );
					}
				},

				set_slide_arrows_visibility = function( current_tab )
				{
					if( current_tab > 1 )
					{
						slide_arrows_wrap.addClass( 'av-visible-prev' );
					}
					else
					{
						slide_arrows_wrap.removeClass( 'av-visible-prev' );
					}

					if( current_tab < tabs.length )
					{
						slide_arrows_wrap.addClass( 'av-visible-next' );
					}
					else
					{
						slide_arrows_wrap.removeClass( 'av-visible-next' );
					}
				},

				set_slide_dots_visibility = function( current_tab )
				{
					slide_dots_wrap.find( 'a' ).removeClass( 'active' );
					slide_dots_wrap.find( 'a' ).eq( current_tab - 1 ).addClass( 'active' );
				},

				swipe_to_next_prev = function(e)
				{
					//	ignore user interaction
					if( slideshowOptions.noNavigation )
					{
						return;
					}

					switch_to_next_prev( e );
				},

				switch_to_next_prev = function( e )
				{
					e.preventDefault();

					var clicked = $( e.currentTarget ),
						current_tab = container.find('.av-active-tab-title');

					//	handle slideshow section -> reroute to slideshow navigation arrows (might be hidden with CSS)
					if( container.hasClass( 'av-slideshow-section' ) )
					{
						if( clicked.hasClass( 'av_prev_tab_section' ) )
						{
							slide_arrows_wrap.find( '.av_prev_tab_section' ).trigger( 'click' );
						}
						else
						{
							slide_arrows_wrap.find( '.av_next_tab_section' ).trigger( 'click' );
						}

						return;
					}

					if( clicked.is('.av_prev_tab_section') )
					{
						if( ! $('body').hasClass('rtl') )
						{
							current_tab.prev('.av-section-tab-title').trigger('click');
						}
						else
						{
							current_tab.next('.av-section-tab-title').trigger('click');
						}
					}
					else
					{
						if( ! $('body').hasClass('rtl') )
						{
							current_tab.next('.av-section-tab-title').trigger('click');
						}
						else
						{
							current_tab.prev('.av-section-tab-title').trigger('click');
						}
					}
				},

				slide_arrows_next_prev = function( e )
				{
					e.preventDefault();

					//	ignore user clicks on slideshow arrows
					if( slideshowOptions.noNavigation && e.originalEvent !== undefined )
					{
						return;
					}

					var clicked = $( e.currentTarget ),
						current_tab = container.find('.av-active-tab-title'),
						tab_nr = current_tab.data('av-tab-section-title'),
						iTab_nr = parseInt( tab_nr, 10 ),
						next = 0;

					if( clicked.hasClass( 'av_prev_tab_section' ) )
					{
						next = ! $('body').hasClass('rtl') ? -1 : 1;
					}
					else
					{
						next = ! $('body').hasClass('rtl') ? 1 : -1;
					}

					var pos = iTab_nr + next;

					if( pos <= 0 || pos > tabs.length )
					{
						//	fallback, if arrows are visible for first or last slide
						if( 'endless' != slideshowOptions.loop_autoplay && 'manual-endless' != slideshowOptions.loop_manual )
						{
							return;
						}

						pos = pos <= 0 ? tabs.length : 1;
					}

					clearTimeoutAutoplay();
					tabs.eq( pos - 1 ).trigger( 'click' );
					init_autoplay();
				},

				slide_dots_change_tab = function( e )
				{
					e.preventDefault();

					var clicked = $( e.currentTarget );

					if( clicked.hasClass( 'active' ) )
					{
						return;
					}

					var tab_nr = clicked.attr( 'href' ).replace( '#', '' ),
						iTab_nr = parseInt( tab_nr, 10 );

					if( iTab_nr > tabs.length )
					{
						return;
					}

					clearTimeoutAutoplay();
					tabs.eq( iTab_nr - 1 ).trigger( 'click' );
					init_autoplay();
				},

				get_init_open = function()
				{
//					removed 5.0
//					if( ! hash && window.location.hash ) var hash = window.location.hash;

					var hash = window.location.hash ? window.location.hash : '',
						deepHash = hash.toLowerCase().replace( '#', '' ),
						open = null;

					if( 'undefined' != typeof( deepLinksToTabs[ deepHash ] ) && '' != deepLinksToTabs[ deepHash ] )
					{
						var hashID = deepLinksToTabs[ deepHash ];
						open = tabs.filter( '[data-av-tab-section-title="' + hashID + '"]' );
					}
					else
					{
						open = tabs.filter( '[href="' + hash + '"]' );
					}

					if( open.length )
					{
						if( ! open.is( '.active_tab' ) )
						{
							open.trigger( 'click' );
						}
					}
					else
					{
						//set correct color
						container.find( '.av-active-tab-title' ).trigger( 'click', true );
					}
				},

				clearTimeoutAutoplay = function()
				{
					if( typeof timeoutIDAutoplay === 'number' )
					{
						clearTimeout( timeoutIDAutoplay );
					}

					timeoutIDAutoplay = null;
				},

				init_autoplay = function()
				{
					if( ! container.hasClass( 'av-slideshow-section' ) )
					{
						return;
					}

					if( true !== slideshowOptions.autoplay )
					{
						tab_outer.removeClass( 'av-slideshow-autoplay' ).addClass( 'av-slideshow-manual' );
					}

					if( 'undefined' == typeof slideshowOptions.loop_autoplay || 'endless' != slideshowOptions.loop_autoplay  )
					{
						slideshowOptions.loop_autoplay = 'once';
					}

					if( 'undefined' == typeof slideshowOptions.interval )
					{
						slideshowOptions.interval = 5;
					}

					if( 'undefined' == typeof slideshowOptions.autoplay || true !== slideshowOptions.autoplay  )
					{
						slideshowOptions.autoplay = false;
						tab_outer.removeClass( 'av-slideshow-autoplay' ).addClass( 'av-slideshow-manual' );
						return;
					}

					clearTimeoutAutoplay();

					timeoutIDAutoplay = setTimeout( function()
					{
						rotate_next_slide();
					}, slideshowOptions.interval * 1000 );
				},

				rotate_next_slide = function()
				{
					var current_tab = container.find('.av-active-tab-title'),
						tab_nr = current_tab.data('av-tab-section-title'),
						iTab_nr = parseInt( tab_nr, 10 ),
						stop = false,
						next = 0;

					timeoutIDAutoplay = null;

					if( 'endless' == slideshowOptions.loop_autoplay )
					{
						if( ! $('body').hasClass('rtl') )
						{
							next = iTab_nr < tabs.length ? iTab_nr + 1 : 1;
						}
						else
						{
							next = iTab_nr > 1 ? iTab_nr - 1 : tabs.length;
						}
					}
					else
					{
						if( ! $('body').hasClass('rtl') )
						{
							stop = iTab_nr == tabs.length;
							next = iTab_nr + 1;
						}
						else
						{
							stop = iTab_nr == 1;
							next = iTab_nr - 1;
						}

						if( stop )
						{
							slideshowOptions.autoplay = false;
							slideshowOptions.loop_autoplay = 'manual';
							tab_outer.removeClass( 'av-slideshow-autoplay' ).addClass( 'av-slideshow-manual' );
							tab_outer.removeClass( 'av-loop-endless' ).addClass( 'av-loop-once' );
							return;
						}
					}

					tabs.eq( next - 1 ).trigger( 'click' );

					timeoutIDAutoplay = setTimeout( function()
					{
						rotate_next_slide();
					}, slideshowOptions.interval * 1000 );
				};

			$.avia_utilities.preload({

				container: current_content,
				single_callback: function()
				{
					tabs.on( 'click', change_tab );
					arrows.on( 'click', switch_to_next_prev );
					slide_arrows.on( 'click', slide_arrows_next_prev );
					slide_dots.on( 'click', slide_dots_change_tab );

					//	implement swipe event
					if( isMobile || isTouchDevice )
					{
						tab_nav.on( 'click', swipe_to_next_prev );
					}

					win.on( 'debouncedresize', set_tab_title_pos );

					win.on( 'hashchange', get_init_open );


					/**
					 * We had to remove av-height-change because this event is recursivly triggered in set_slide_height and lead to performance problems
					 * AND broken layout - content was not displayed completly
					 *
					 * Content elements that can can change their height and trigger av-height-change should trigger this additional event after to
					 * allow layout elements like tab section to react on this and then call av-height-change by themself
					 *
					 * @since 4.2.3
					 */
					win.on( 'debouncedresize av-content-el-height-changed', set_slide_height );

					set_min_width();
					set_slide_height();
					get_init_open();
					init_autoplay();
				}
			});

			if( isMobile || isTouchDevice )
			{
				if( ! slideshowOptions.noNavigation )
				{
					content_wrap.avia_swipe_trigger( { prev:'.av_prev_tab_section', next:'.av_next_tab_section' } );
				}
			}

			//	preload has some delay - try to build a correct layout
			set_slide_height();
		});
	};

}(jQuery));
