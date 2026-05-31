from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import EmailMessage, send_mail
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views import View, generic
from django.views.decorators.csrf import csrf_exempt

import json
import stripe

from authentication.models import User

from .forms import BlogPostForm, MessageForm, RequestDemoForm, TicketForm
from .models import (
    BlogPost,
    CreditTransaction,
    Fulfillment,
    Message,
    Service,
    ServiceBooking,
    Ticket,
)


class ContactUsView(View):
    def get(self, request):
        return render(request, 'pages/contact_us.html', {'title': 'Contact Us'})


class RequestDemoView(View):
    template_name = 'pages/request_demo.html'

    def get_context(self, form=None, success_message=None):
        return {
            'title': 'Book a Demo',
            'meta_title': 'AAPPLIFY | Map Your Agent Control Gaps',
            'meta_description': 'Map one AI-agent, access, data, cloud, or change workflow and see where ownership, scope, approval, remediation, exception, and audit evidence are missing.',
            'form': form or RequestDemoForm(),
            'success_message': success_message,
        }

    def get(self, request):
        return render(request, self.template_name, self.get_context())

    def post(self, request):
        form = RequestDemoForm(request.POST)
        if not form.is_valid():
            return render(request, self.template_name, self.get_context(form=form))

        cleaned = form.cleaned_data
        message_body = (
            "New AAPPLIFY control assurance demo request\n\n"
            f"Name: {cleaned['name']}\n"
            f"Work email: {cleaned['work_email']}\n"
            f"Company: {cleaned['company']}\n"
            f"Role: {cleaned['role']}\n"
            f"Identity / security tools: {cleaned['ci_tool']}\n"
            f"Change / workflow tools: {cleaned['test_tool']}\n"
            f"Data / observability tools: {cleaned['observability_tool']}\n"
            f"Departments / apps in scope: {cleaned['number_of_apps_pipelines']}\n"
            "Highest-priority risk or workflow:\n"
            f"{cleaned['biggest_release_blocker']}\n"
        )

        try:
            demo_email = EmailMessage(
                subject=f"Request Demo: {cleaned['company']} - {cleaned['name']}",
                body=message_body,
                from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', settings.EMAIL_HOST_USER),
                to=['support@aapplify.com'],
                reply_to=[cleaned['work_email']],
            )
            demo_email.send(fail_silently=False)
        except Exception:
            form.add_error(None, 'We could not submit your request right now. Please try again or email support@aapplify.com.')
            return render(request, self.template_name, self.get_context(form=form))

        success_message = (
            "Thanks. Your request is in and our team will follow up to confirm the "
            "best path for a focused control assurance pilot."
        )
        return render(request, self.template_name, self.get_context(success_message=success_message))


# Solutions pages
class SolutionQualityOpsView(View):
    def get(self, request):
        return render(request, 'pages/solutions/qualityops.html', {'title': 'QualityOps Signal Hub'})

class SolutionIncidentView(View):
    def get(self, request):
        return render(request, 'pages/solutions/incident.html', {'title': 'Incident Triage & Response for SIEM'})

class SolutionDataQualityView(View):
    def get(self, request):
        return render(request, 'pages/solutions/data_quality.html', {'title': 'Data Quality & Pipeline Management'})

class SolutionRiskControlsView(View):
    def get(self, request):
        return render(request, 'pages/solutions/risk_controls.html', {'title': 'Risk & Controls Monitoring'})

class SolutionCustomerSupportView(View):
    def get(self, request):
        return render(request, 'pages/solutions/customer_support.html', {'title': 'Customer Support Signal Radar'})

class SolutionReleaseGuardrailsView(View):
    def get(self, request):
        return render(request, 'pages/solutions/release_guardrails.html', {'title': 'Change Guardrails & Controls'})

# Knowledge Base pages
class KBGettingStartedView(View):
    def get(self, request):
        return render(request, 'pages/knowledge_base/getting_started.html', {'title': 'Getting Started'})

class KBAPIReferenceView(View):
    def get(self, request):
        return render(request, 'pages/knowledge_base/api_reference.html', {'title': 'API Reference'})

class KBFAQView(View):
    def get(self, request):
        return render(request, 'pages/knowledge_base/faq.html', {'title': 'FAQ'})

class KBContactSupportView(View):
    def get(self, request):
        return render(request, 'pages/knowledge_base/contact_support.html', {'title': 'Contact Support'})

    def post(self, request):
        name = request.POST.get('customer_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        reason = request.POST.get('reason')
        message_body = f"Customer Name: {name}\nEmail: {email}\nPhone: {phone}\nReason: {reason}"
        send_mail(
            subject=f"Support Request from {name}",
            message=message_body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=['support@aapplify.com'],
            fail_silently=False,
        )
        return render(request, 'pages/knowledge_base/contact_support.html', {
            'title': 'Contact Support',
            'message': 'Your support request has been sent. Our team will contact you soon.'
        })

# About Us pages
class AboutCompanyHistoryView(View):
    def get(self, request):
        return render(request, 'pages/about_us/company_history.html', {'title': 'Company History'})

class AboutTeamView(View):
    def get(self, request):
        return render(request, 'pages/about_us/team.html', {'title': 'Team'})

class AboutCareersView(View):
    def get(self, request):
        return render(request, 'pages/about_us/careers.html', {'title': 'Careers'})


# Product pages
class ProductConnectView(View):
    def get(self, request):
        return render(request, 'pages/products/connect.html', {'title': 'AAPPLIFY Connect'})

class ProductNormalizeView(View):
    def get(self, request):
        return render(request, 'pages/products/normalize.html', {'title': 'AAPPLIFY Normalize'})

class ProductSignalsView(View):
    def get(self, request):
        return render(request, 'pages/products/signals.html', {'title': 'AAPPLIFY Signals'})

class ProductFlowView(View):
    def get(self, request):
        return render(request, 'pages/products/flow.html', {'title': 'AAPPLIFY Flow'})

class ProductGuardView(View):
    def get(self, request):
        return render(request, 'pages/products/guard.html', {
            'title': 'AAPPLIFY Guard',
            'meta_title': 'AAPPLIFY Guard | Exception Governance for AI-Agent Actions',
            'meta_description': 'AAPPLIFY Guard tracks temporary risk acceptance, compensating controls, approvals, expiration dates, renewal decisions, escalation paths, and audit evidence for AI-agent actions.',
        })

class ProductRunbooksView(View):
    def get(self, request):
        return render(request, 'pages/products/runbooks.html', {'title': 'AAPPLIFY Runbooks'})

class ProductConsoleView(View):
    def get(self, request):
        return render(request, 'pages/products/console.html', {'title': 'AAPPLIFY Console'})

stripe.api_key = settings.STRIPE_SECRET_KEY
endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

# Create your views here.
class HomeView(View):
    def get(self, request):
        return render(request, 'pages/home.html', {
            'title': 'AI Agent Control Assurance',
            'meta_title': 'AAPPLIFY | AI Agent Control Assurance',
            'meta_description': 'Prove AI agents and autonomous workflows were owned, scoped, approved, remediated, excepted, and audit-ready before they touched enterprise systems.',
        })

class ReleaseReadinessLandingView(View):
    def get(self, request):
        return render(request, 'pages/release_readiness_landing.html', {
            'title': 'AI-Agent Production Readiness Use Case',
            'meta_title': 'AAPPLIFY | AI-Agent Production Readiness Use Case',
            'meta_description': 'Use AAPPLIFY to approve, hold, remediate, or except AI agents before they enter production workflows.',
        })

def domain_cards(active_domain):
    cards = [
        {
            'name': 'Change',
            'title': 'Agent production readiness',
            'copy': 'Approve, hold, remediate, or except AI agents before production.',
            'href': reverse('landing_release_readiness'),
        },
        {
            'name': 'Identity',
            'title': 'Agent access assurance',
            'copy': 'Review agent identities, service accounts, and risky grants.',
            'href': reverse('landing_identity'),
        },
        {
            'name': 'Data',
            'title': 'Agent data assurance',
            'copy': 'Map agent sensitive-data reach to policy and controls.',
            'href': reverse('landing_data'),
        },
        {
            'name': 'Security',
            'title': 'Agent remediation evidence',
            'copy': 'Connect risky findings to remediation proof.',
            'href': reverse('landing_security'),
        },
    ]
    for card in cards:
        card['active'] = card['name'].lower() == active_domain
    return cards

class IdentityLandingView(View):
    def get(self, request):
        return render(request, 'pages/domain_use_case.html', {
            'title': 'AI-Agent Access Assurance Use Case',
            'meta_title': 'AAPPLIFY | AI-Agent Access Assurance Use Case',
            'meta_description': 'Use AAPPLIFY to prove AI-agent access, service accounts, privileged grants, third-party users, and access changes were owned, scoped, approved, time-bound, remediated, or revoked.',
            'eyebrow': 'AI-agent access assurance',
            'hero_title': 'Prove AI-agent access was owned, scoped, approved, and time-bound.',
            'hero_copy': 'Use this workflow when AI agents, automations, service accounts, delegated users, roles, or emergency grants can create security risk. AAPPLIFY connects identity, change, data, security, and policy context into one auditable access decision.',
            'placement_note': 'Start with agent access assurance. The same evidence model extends across sensitive data, cloud exposure, third-party activity, and production change.',
            'console_label': 'Agent Access Workflow',
            'console_status': 'Review required',
            'console_title': 'Privileged Access Review',
            'console_copy': 'An AI agent receives a production role grant that touches a sensitive data system and lacks owner approval evidence.',
            'metrics': [
                {'label': 'Privilege drift', 'value': '7 accounts'},
                {'label': 'Service accounts', 'value': '3 stale owners'},
                {'label': 'Data access', 'value': '2 sensitive stores'},
                {'label': 'Controls', 'value': 'MFA + approval missing'},
            ],
            'score': '82',
            'score_label': 'Identity exposure score',
            'score_drivers': 'Top drivers: privileged grant, sensitive data reach, stale owner, missing approval',
            'fit_title': 'Agent access is the fastest place to prove control assurance.',
            'fit_copy': 'Use it for agent access assurance, then extend the same evidence workflow across change, data, security, and third-party activity.',
            'domain_cards': domain_cards('identity'),
            'signals_title': 'Identity signals that are worth action.',
            'signals_copy': 'AAPPLIFY filters identity events through ownership, data sensitivity, change windows, policies, and security posture so teams know which access changes need review.',
            'signals': [
                {'kicker': 'Agent access', 'title': 'Agent privilege changed outside policy', 'copy': 'Detects role grants, group changes, delegated access, or entitlement expansion that conflicts with policy or expected ownership.'},
                {'kicker': 'Service accounts', 'title': 'Non-human identity risk', 'copy': 'Surfaces stale owners, broad scopes, unused credentials, and agent identities tied to critical systems.'},
                {'kicker': 'Sensitive reach', 'title': 'Agent access touches protected data', 'copy': 'Connects identity permissions to data classification, lineage, and control requirements.'},
            ],
            'workflow_title': 'Turn access signals into control evidence.',
            'workflow_copy': 'Route identity risks to owners, require approvals, create remediation tasks, and preserve evidence for audits.',
            'workflow_steps': [
                {'number': 'Step 1', 'title': 'Connect', 'copy': 'Ingest IdP, PAM, HRIS, ticket, data, agent inventory, and cloud logs.'},
                {'number': 'Step 2', 'title': 'Signal', 'copy': 'Prioritize risky agent grants, stale owners, excessive scope, and policy conflicts.'},
                {'number': 'Step 3', 'title': 'Orchestrate', 'copy': 'Trigger owner review, approval, revocation, or exception workflow.'},
                {'number': 'Step 4', 'title': 'Control', 'copy': 'Capture MFA, SoD, approval, and access-review evidence.'},
            ],
            'cta_title': 'Map your first agent access assurance workflow.',
            'cta_copy': 'Map one agent access workflow and see how AAPPLIFY connects identity data, policies, signals, workflows, and evidence.',
        })

class DataLandingView(View):
    def get(self, request):
        return render(request, 'pages/domain_use_case.html', {
            'title': 'AI-Agent Sensitive Data Assurance Use Case',
            'meta_title': 'AAPPLIFY | AI-Agent Sensitive Data Assurance Use Case',
            'meta_description': 'Use AAPPLIFY to prove AI-agent access to sensitive data had data-owner approval, privacy review, policy validation, access-control evidence, and remediation.',
            'eyebrow': 'AI-agent sensitive data assurance',
            'hero_title': 'Prove AI-agent access to sensitive data had policy approval and audit evidence.',
            'hero_copy': 'Use this workflow when AI agents, automations, service accounts, or delegated identities can touch customer data, PII, financial data, healthcare data, production logs, or regulated datasets. AAPPLIFY connects data, identity, change, security, and policy context into one evidence-backed decision.',
            'placement_note': 'Start with agent sensitive-data assurance. The same evidence model extends across access, change, cloud exposure, and production workflows.',
            'console_label': 'Agent Data Workflow',
            'console_status': 'Policy match',
            'console_title': 'Sensitive Data Movement Review',
            'console_copy': 'An AI agent can query customer records in a new analytics workflow with policy requirements and owner approval pending.',
            'metrics': [
                {'label': 'Data class', 'value': 'Customer PII'},
                {'label': 'Movement', 'value': 'New destination'},
                {'label': 'Identity', 'value': '2 new readers'},
                {'label': 'Controls', 'value': 'Retention review needed'},
            ],
            'score': '76',
            'score_label': 'Data policy risk score',
            'score_drivers': 'Top drivers: sensitive classification, new destination, expanded readers, retention policy gap',
            'fit_title': 'Sensitive-data access is where AI-agent risk becomes business risk.',
            'fit_copy': 'Use it for agent data-policy assurance, then extend the same evidence workflow across identity, change, and security.',
            'domain_cards': domain_cards('data'),
            'signals_title': 'Data signals that connect policy to operations.',
            'signals_copy': 'AAPPLIFY filters data events through classification, lineage, identity access, change context, and imported policy files.',
            'signals': [
                {'kicker': 'Classification', 'title': 'Agent reaches sensitive data', 'copy': 'Detects when protected data enters an agent workflow, report, pipeline, or app workflow that needs control review.'},
                {'kicker': 'Policy files', 'title': 'Procedure becomes a control draft', 'copy': 'Reads existing policies and procedures to draft workflow requirements, approvals, and controls.'},
                {'kicker': 'Access + lineage', 'title': 'Agent data reach changes', 'copy': 'Combines identity and lineage context so teams can see which agent can touch sensitive data and why.'},
            ],
            'workflow_title': 'Turn agent data signals into policy-compliant action.',
            'workflow_copy': 'Route agent data risks to owners, validate controls, require approvals, and preserve policy evidence.',
            'workflow_steps': [
                {'number': 'Step 1', 'title': 'Connect', 'copy': 'Ingest data catalogs, warehouses, DLP, tickets, identity, and policy files.'},
                {'number': 'Step 2', 'title': 'Signal', 'copy': 'Prioritize sensitive movement, access expansion, and policy conflicts.'},
                {'number': 'Step 3', 'title': 'Orchestrate', 'copy': 'Trigger owner review, privacy approval, remediation, or exception workflow.'},
                {'number': 'Step 4', 'title': 'Control', 'copy': 'Capture retention, access, region, approval, and audit evidence.'},
            ],
            'cta_title': 'Map your first agent data assurance workflow.',
            'cta_copy': 'Map one sensitive-data workflow and see how AAPPLIFY turns policies and telemetry into audit-ready evidence.',
        })

class SecurityLandingView(View):
    def get(self, request):
        return render(request, 'pages/domain_use_case.html', {
            'title': 'AI-Agent Remediation Evidence Use Case',
            'meta_title': 'AAPPLIFY | AI-Agent Remediation Evidence Use Case',
            'meta_description': 'Use AAPPLIFY to prove risky AI-agent findings, vulnerabilities, posture gaps, and exposure paths were owned, remediated, excepted, escalated, or closed with evidence.',
            'eyebrow': 'AI-agent remediation evidence',
            'hero_title': 'Prove risky AI-agent findings were remediated, excepted, or closed with evidence.',
            'hero_copy': 'Use this workflow when agent findings, excessive permissions, vulnerabilities, posture gaps, exposed APIs, incidents, or risky changes need action. AAPPLIFY connects security, identity, data, change, and policy context into one evidenced remediation path.',
            'placement_note': 'Start with agent remediation evidence. The same evidence model extends across access, data, change, cloud, and broader security workflows.',
            'console_label': 'Agent Remediation Workflow',
            'console_status': 'Escalate',
            'console_title': 'Exposure Path Review',
            'console_copy': 'An agent-access path has elevated identity reach, sensitive data access, and an unapproved configuration change.',
            'metrics': [
                {'label': 'Finding', 'value': 'Critical CVE'},
                {'label': 'Identity', 'value': 'Privileged path'},
                {'label': 'Data', 'value': 'PII reachable'},
                {'label': 'Change', 'value': 'Config drift'},
            ],
            'score': '91',
            'score_label': 'Security exposure score',
            'score_drivers': 'Top drivers: critical finding, privileged reach, sensitive data, unapproved drift',
            'fit_title': 'Agent remediation evidence connects security findings to proof of closure.',
            'fit_copy': 'Use it for agent exposure paths, then extend the same evidence workflow across identity, data, and change.',
            'domain_cards': domain_cards('security'),
            'signals_title': 'Security signals that move beyond alert volume.',
            'signals_copy': 'AAPPLIFY filters findings through identity reach, data sensitivity, change history, controls, and remediation ownership.',
            'signals': [
                {'kicker': 'Exposure path', 'title': 'Agent finding connects to sensitive systems', 'copy': 'Correlates vulnerabilities and posture gaps with agent identity access, data reach, and asset ownership.'},
                {'kicker': 'Control gap', 'title': 'Security control evidence is missing', 'copy': 'Flags missing approvals, compensating controls, remediation records, or policy evidence.'},
                {'kicker': 'Incident workflow', 'title': 'Risk needs escalation or remediation', 'copy': 'Routes the right action to security, platform, identity, data, or application owners.'},
            ],
            'workflow_title': 'Turn agent security signals into remediation proof.',
            'workflow_copy': 'Route agent exposure paths to owners, require approvals, track remediation, and preserve evidence for security and compliance review.',
            'workflow_steps': [
                {'number': 'Step 1', 'title': 'Connect', 'copy': 'Ingest security findings, cloud posture, identity, data, tickets, and change logs.'},
                {'number': 'Step 2', 'title': 'Signal', 'copy': 'Prioritize findings with reachability, sensitive data, and control context.'},
                {'number': 'Step 3', 'title': 'Orchestrate', 'copy': 'Trigger remediation, escalation, exception, or compensating-control workflows.'},
                {'number': 'Step 4', 'title': 'Control', 'copy': 'Capture evidence for owners, approvals, posture, remediation, and audit.'},
            ],
            'cta_title': 'Map your first agent remediation evidence workflow.',
            'cta_copy': 'Map one exposure workflow and see how AAPPLIFY turns findings into governed remediation.',
        })

class AapplifyLandingView(View):
    def get(self, request):
        return render(request, 'pages/aapplify_landing.html', {
            'title': 'AAPPLIFY',
            'meta_title': 'AAPPLIFY | AI Agent Control Assurance',
            'meta_description': 'AAPPLIFY proves AI agents and autonomous workflows were owned, scoped, approved, remediated, excepted, and audit-ready before they touched enterprise systems.'
        })

class AIAgentOrchestrationLandingView(View):
    def get(self, request):
        return render(request, 'pages/ai_agent_orchestration_landing.html', {
            'title': 'AAPPLIFY | AI-Agent Action Assurance',
            'meta_title': 'AAPPLIFY | AI-Agent Action Assurance',
            'meta_description': 'Govern AI agents, automations, service accounts, and delegated identities before they access systems, call APIs, touch data, or enter production workflows.'
        })

class AboutView(View):
    def get(self, request):
        return render(request, 'pages/about.html', {
            'title': 'Why AAPPLIFY',
            'meta_title': 'AAPPLIFY | Why We Built AI Agent Control Assurance',
            'meta_description': 'Learn why AAPPLIFY was built to prove AI agents and high-risk enterprise actions were owned, scoped, approved, remediated, excepted, and audit-ready.',
        })
    
class ShortDescriptionView(View):
    def get(self, request):
        return render(request, 'pages/home/herosection.html',  {'title': 'Short Description'})

class LongDescriptionView(View):
    def get(self, request):
        return render(request, 'pages/home/unlockai.html',  {'title': 'Long Description'})

class TosView(View):
    def get(self, request):
        return render(request, 'pages/tos.html', {
            'title': 'Website Terms',
            'meta_title': 'AAPPLIFY | Website Terms',
            'meta_description': 'Website terms governing use of aapplify.com and related public materials.',
        })


class PrivacyView(View):
    def get(self, request):
        return render(request, 'pages/privacy.html', {
            'title': 'Privacy Policy',
            'meta_title': 'AAPPLIFY | Privacy Policy',
            'meta_description': 'How AAPPLIFY collects, uses, and protects personal information across demo requests, onboarding, integrations, and product usage.',
        })

class BlogView(View):
    def get(self, request, blog_id=None):
        if blog_id:
            # Get a single blog post by ID
            blog = get_object_or_404(BlogPost, id=blog_id)
            return render(request, 'pages/blog_detail.html', {'blog': blog, 'title': 'Blog'})

        # Get all blog posts if no blog_id is provided
        blogs = BlogPost.objects.filter(is_accepted=True)
        return render(request, 'pages/blog.html', {'blogs': blogs, 'title': 'Blog'})


class ContactView(View):
    def get(self, request):
        return render(request, 'pages/contact.html', {'title': 'Contact'})

class FAQView(View):
    def get(self, request):
        return render(request, 'pages/faq.html', {
            'title': 'AI Agent Control Assurance FAQ',
            'meta_title': 'AAPPLIFY | AI Agent Control Assurance FAQ',
            'meta_description': 'Answers to common questions about AI-agent ownership, identity, access scope, policy decisions, remediation, exceptions, audit-ready evidence, pilots, and integrations.',
        })


class AddBlogView(LoginRequiredMixin, View):
    login_url = '/auth/login/'
    # redirect_field_name = 'redirect_to'


    def get(self, request, slug=None):
        form = BlogPostForm()

        return render(request, 'pages/addblog.html', {'form': form, 'title': 'Add Blog'})

    def post(self, request, slug=None):
        form = BlogPostForm(request.POST, request.FILES)
        # form["created_by"] = request.user.pk
        print(request.user)
        if form.is_valid():
            blog_post = form.save(commit=False)
            blog_post.created_by = request.user
            blog_post.save()
            form = BlogPostForm()
            messages.success(request, 'Your form has been submitted successfully!')
            return redirect(reverse('add_blog'))
        print(form.is_valid())
        print(form.errors)

        # Form is not valid, render the form with errors
        return render(request, 'pages/addblog.html', {'form': form})

def get_random_staff():
    pass
class TokenView(LoginRequiredMixin, View):
    login_url = '/auth/login/'

    def get(self, request):
        # Fetch the tickets for the logged-in user
        if request.user.is_staff:
            tickets = Ticket.objects.all()
        else:
            tickets = Ticket.objects.filter(user=request.user)
        form = TicketForm()
        return render(request, 'pages/token.html', context={"form": form, "tickets": tickets, "title":"Token"})


    def post(self, request, slug=None):
        form = TicketForm(request.POST)
        if form.is_valid():
            message = form.cleaned_data["message"]
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.staff = get_random_staff()
            ticket.save()

            Message.objects.create(
                content=message,
                user=request.user,
                room=ticket
            )
            form = TicketForm()
            return redirect(reverse('main_token'))
        print(form.is_valid())
        print(form.errors)

        # Form is not valid, render the form with errors
        return render(request, 'pages/addblog.html', {'form': form})

class TicketDetailView(View):
    def get(self, request, pk):
        ticket = get_object_or_404(Ticket, pk=pk)
        messages = Message.objects.filter(room=ticket).reverse()
        form = MessageForm()  # Initialize the form
        return render(request, 'pages/ticket_detail.html', {'ticket': ticket, 'messages': messages, 'form': form, "title":"token"})

    def post(self, request, pk):
        ticket = get_object_or_404(Ticket, pk=pk)
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.room = ticket
            message.user = request.user
            # Automatically flag staff messages
            if request.user.is_staff:
                message.is_staff_response = True
            message.save()
            return redirect('ticket_detail', pk=ticket.id)

        messages = Message.objects.filter(room=ticket)
        return render(request, 'pages/ticket_detail.html', {'ticket': ticket, 'messages': messages, 'form': form})



class BlogPostView(View):
    def get(self, request, slug=None):
        if slug:
            # Edit an existing blog post
            blog_post = get_object_or_404(BlogPost, slug=slug)
            form = BlogPostForm(instance=blog_post)
        else:
            # Create a new blog post
            form = BlogPostForm()

        return render(request, 'pages/blog_post_form.html', {'form': form, "title":"Blog"})

    def post(self, request, slug=None):
        if slug:
            # Update an existing blog post
            blog_post = get_object_or_404(BlogPost, slug=slug)
            form = BlogPostForm(request.POST, request.FILES, instance=blog_post)
        else:
            # Create a new blog post
            form = BlogPostForm(request.POST, request.FILES)

        if form.is_valid():
            blog_post = form.save()
            return redirect(reverse('blog_post_detail', args=[blog_post.slug]))

        return render(request, 'pages/blog_post_form.html', {'form': form})

class ProfileView(LoginRequiredMixin, View):
    login_url = '/auth/login/'

    def get(self, request):
        profile = get_object_or_404(User, email=request.user)
        blogs = BlogPost.objects.filter(created_by=profile)
        booking = ServiceBooking.objects.filter(user=profile)

        context = {
        'profile': profile,
        'blogs': blogs,
        'booking': booking,
        'title': profile
            }

        return render(request, 'pages/profile.html', context)

class ServiceView(View):
    def get(self, request, service_id=None):
        if service_id:
            service = get_object_or_404(Service, id=service_id)
            print(service)
            return render(request, 'pages/service_detail.html', {'service': service, 'title':'service'})

        # List all services
        services = Service.objects.all()
        return render(request, 'pages/services.html', {'services': services, 'title':'Service'})


class CreateCheckoutSessionView(generic.View):
    def post(self, *args, **kwargs):
        try:
            host = self.request.get_host()
            # Get service price dynamically from POST data
            service_id = self.request.POST['service_id']

            # Fetch service details from the database
            service = get_object_or_404(Service, id=int(service_id))

            # Convert price to an integer (in the smallest currency unit, such as poisha for BDT)
            price_in_cents = int(float(service.price) * 100)

            # Create a Checkout Session
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card', 'us_bank_account'],
                line_items=[
                    {
                        'price_data': {
                            'currency': 'usd',
                            'unit_amount': price_in_cents,  # Unit amount in the smallest currency unit
                            'product_data': {
                                'name': service.title,  # Name of the product
                            },
                        },
                        'quantity': 1,
                    },
                ],
                mode='payment',
                success_url=f"http://{host}{reverse('success', kwargs={'booking_id': service.id})}",
                cancel_url=f"http://{host}{reverse('cancel')}",
                metadata={
                    'service_id': str(service.id),
                    'user_id': str(self.request.user.id)  # Assuming the user is logged in
                }
            )

            return redirect(checkout_session.url, code=303)
        except stripe.error.StripeError as e:
            return JsonResponse({'error': str(e)}, status=400)
        except Exception as e:
            return JsonResponse({'error': f'An error occurred: {str(e)}'}, status=500)


def success(request, booking_id):

    service = get_object_or_404(Service, id=int(booking_id))
    print(service)
    print(request.user)

    # Create a booking record for the user
    booking = ServiceBooking.objects.create(
        service=service,
        user=request.user,
        title=service.title,
        price=service.price,
        credit_quantity=service.credit_quantity,
        status='confirmed',  # Assuming the booking is confirmed after payment
        booking_date=timezone.now()
    )

    print(booking)
    return render(request, "pages/success.html", {"booking":booking})

def cancel(request):
    return render(request, "pages/cancel.html")


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
        print(event)
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the event
    if event['type'] == 'checkout.session.completed' or event['type'] == 'checkout.session.async_payment_succeeded':
        session = event['data']['object']
        fulfill_checkout(session)

    return HttpResponse(status=200)

def fulfill_checkout(session):
    session_id = session['id']

    # Check if the fulfillment has already been done for this session
    if Fulfillment.objects.filter(session_id=session_id, fulfilled=True).exists():
        print(f"Session {session_id} has already been fulfilled.")
        return

    # Retrieve the line items and metadata from the session
    checkout_session = stripe.checkout.Session.retrieve(
        session_id,
        expand=['line_items'],
    )

    # Extract service details from metadata
    service_id = checkout_session.metadata['service_id']
    user_id = checkout_session.metadata['user_id']

    # Fetch the service and user from the database
    service = get_object_or_404(Service, id=int(service_id))
    user = get_object_or_404(User, id=int(user_id))

    # Record the fulfillment in the Fulfillment model
    Fulfillment.objects.create(
        session_id=session_id,
        fulfilled=True
    )

    user.credits += service.credit_quantity
    user.save()
    CreditTransaction.objects.create(
        user=user,
        credits_earned=service.credit_quantity,

        log=f"Service {service.title} booked."
    )

    print(f"Service {service.title} booked for user {user.username}.")

@csrf_exempt
def save_workflow(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        return JsonResponse({"message": "Workflow saved successfully!", "data": data})
    return JsonResponse({"error": "Invalid request"}, status=400)
