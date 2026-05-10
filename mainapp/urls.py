
from django.urls import path
from .views import *

urlpatterns = [
    path('', HomeView.as_view(), name='main_home'),
    path('landing/release-readiness/', ReleaseReadinessLandingView.as_view(), name='landing_release_readiness'),
    path('landing/identity/', IdentityLandingView.as_view(), name='landing_identity'),
    path('landing/data/', DataLandingView.as_view(), name='landing_data'),
    path('landing/security/', SecurityLandingView.as_view(), name='landing_security'),
    path('landing/aapplify/', AapplifyLandingView.as_view(), name='landing_aapplify'),
    path('landing/ai-agent-orchestration/', AIAgentOrchestrationLandingView.as_view(), name='landing_ai_agent_orchestration'),
    path('profile/', ProfileView.as_view(), name='main_profile'),
    path('about/', AboutView.as_view(), name='main_about'),
    path('tos/', TosView.as_view(), name='main_tos'),
    path('privacy/', PrivacyView.as_view(), name='main_privacy'),
    path('blog/', BlogView.as_view(), name='main_blog'),
    path('blog/<int:blog_id>/', BlogView.as_view(), name='blog-detail'),
    path('contact/', ContactView.as_view(), name='main_contact'),
    path('shortD/', ShortDescriptionView.as_view(), name='main_contact'),
    path('longD/', LongDescriptionView.as_view(), name='main_contact'),
    path('faq/',FAQView.as_view(), name='main_faq'),
    path('service/', ServiceView.as_view(), name='main_services'),
    path('services/<int:service_id>/', ServiceView.as_view(), name='service-detail'),
    path('addblog/', AddBlogView.as_view(), name='add_blog'),
    path('blog/<slug:slug>/', AddBlogView.as_view(), name='edit_blog'),  # Use the same view for editing
    path('token/', TokenView.as_view(), name='main_token'),
    path('create-checkout-session/', CreateCheckoutSessionView.as_view(), name='create_checkout_session'),
    path('success/<int:booking_id>/', success, name='success'),
    path('cancel/', cancel, name='cancel'),
    path('tickets/<int:pk>/', TicketDetailView.as_view(), name='ticket_detail'),
    path('stripe/webhook', stripe_webhook, name='stripe_webhook'),
    # path('blog/<slug:slug>/detail/', BlogPostDetailView.as_view(), name='blog_post_detail'),

    # Product pages
    path('products/connect/', ProductConnectView.as_view(), name='product_connect'),
    path('products/normalize/', ProductNormalizeView.as_view(), name='product_normalize'),
    path('products/signals/', ProductSignalsView.as_view(), name='product_signals'),
    path('products/flow/', ProductFlowView.as_view(), name='product_flow'),
    path('products/guard/', ProductGuardView.as_view(), name='product_guard'),
    path('products/runbooks/', ProductRunbooksView.as_view(), name='product_runbooks'),
    path('products/console/', ProductConsoleView.as_view(), name='product_console'),

    # Solutions pages
    path('solutions/qualityops/', SolutionQualityOpsView.as_view(), name='solution_qualityops'),
    path('solutions/incident/', SolutionIncidentView.as_view(), name='solution_incident'),
    path('solutions/data-quality/', SolutionDataQualityView.as_view(), name='solution_data_quality'),
    path('solutions/risk-controls/', SolutionRiskControlsView.as_view(), name='solution_risk_controls'),
    path('solutions/customer-support/', SolutionCustomerSupportView.as_view(), name='solution_customer_support'),
    path('solutions/release-guardrails/', SolutionReleaseGuardrailsView.as_view(), name='solution_release_guardrails'),

    # Knowledge Base pages
    path('knowledge-base/getting-started/', KBGettingStartedView.as_view(), name='kb_getting_started'),
    path('knowledge-base/api-reference/', KBAPIReferenceView.as_view(), name='kb_api_reference'),
    path('knowledge-base/faq/', KBFAQView.as_view(), name='kb_faq'),
    path('knowledge-base/contact-support/', KBContactSupportView.as_view(), name='kb_contact_support'),

    # About Us pages
    path('about-us/company-history/', AboutCompanyHistoryView.as_view(), name='about_company_history'),
    path('about-us/team/', AboutTeamView.as_view(), name='about_team'),
    path('about-us/careers/', AboutCareersView.as_view(), name='about_careers'),
    # Contact Us and Request Demo pages
    path('contact-us/', ContactUsView.as_view(), name='contact_us'),
    path('request-demo/', RequestDemoView.as_view(), name='request_demo'),
]
