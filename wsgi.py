import linkapp.link
import linkapp.tag
import linkapp.authentication
import linkapp.readinglist
import linkapp.gateway

tag_service = linkapp.tag.wsgi.TagMicroservice(linkapp.tag.config.TagConfig())
link_service = linkapp.link.wsgi.LinkMicroservice(linkapp.link.config.LinkConfig())
auth_service = linkapp.authentication.wsgi.AuthenticationMicroservice(linkapp.authentication.config.AuthenticationConfig())
readinglist_service = linkapp.readinglist.wsgi.ReadinglistMicroservice(linkapp.readinglist.config.ReadinglistConfig())
gateway_service = linkapp.gateway.wsgi.GatewayService(linkapp.gateway.config.GatewayConfig())