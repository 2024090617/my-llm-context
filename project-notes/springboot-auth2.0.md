### Spring Boot集成OAuth2.0认证的步骤

OAuth2.0是一种开放标准的授权协议，允许用户授权第三方应用访问他们的资源而无需共享密码。在Spring Boot中集成OAuth2.0可以使用Spring Security OAuth2模块，下面介绍具体步骤：

### 1. 添加依赖

首先在 `pom.xml`中添加必要的依赖：

```xml
<dependencies>
    <!-- Spring Boot Security -->
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-security</artifactId>
    </dependency>
  
    <!-- Spring Security OAuth2 Client -->
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-oauth2-client</artifactId>
    </dependency>
  
    <!-- Spring Web -->
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-web</artifactId>
    </dependency>
  
    <!-- Thymeleaf (可选，用于视图渲染) -->
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-thymeleaf</artifactId>
    </dependency>
</dependencies>
```

### 2. 配置OAuth2客户端

在 `application.properties`或 `application.yml`中配置OAuth2客户端信息：

```yaml
spring:
  security:
    oauth2:
      client:
        registration:
          github:  # 认证提供商ID，可以是github、google、facebook等
            client-id: your-client-id  # 替换为你的客户端ID
            client-secret: your-client-secret  # 替换为你的客户端密钥
            scope:
              - read:user  # 请求的权限范围
        provider:
          github:
            authorization-uri: https://github.com/login/oauth/authorize  # 授权端点
            token-uri: https://github.com/login/oauth/access_token  # 令牌端点
            user-info-uri: https://api.github.com/user  # 用户信息端点
```

如果你使用的是其他OAuth2提供商（如Google、Facebook等），需要相应调整配置信息。

### 3. 配置Spring Security

创建一个安全配置类来配置OAuth2登录：

```java
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.web.SecurityFilterChain;

@Configuration
public class SecurityConfig {

    @Bean
    public SecurityFilterChain securityFilterChain(HttpSecurity http) throws Exception {
        http
            .authorizeRequests()
                .antMatchers("/", "/login").permitAll()  // 允许匿名访问的路径
                .anyRequest().authenticated()  // 其他路径需要认证
                .and()
            .oauth2Login()  // 启用OAuth2登录
                .defaultSuccessUrl("/home")  // 登录成功后跳转的路径
                .and()
            .logout()
                .logoutSuccessUrl("/");  // 登出后跳转的路径
              
        return http.build();
    }
}
```

### 4. 创建控制器

创建一个简单的控制器来处理请求：

```java
import org.springframework.security.oauth2.client.authentication.OAuth2AuthenticationToken;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.Map;

@RestController
public class HomeController {

    @GetMapping("/")
    public String index() {
        return "欢迎来到登录页面，请点击登录按钮进行认证";
    }

    @GetMapping("/home")
    public String home(OAuth2AuthenticationToken authentication) {
        // 获取用户信息
        Map<String, Object> attributes = authentication.getPrincipal().getAttributes();
        String name = (String) attributes.get("name");
        String login = (String) attributes.get("login");
      
        return "欢迎回来，" + name + " (" + login + ")";
    }
}
```

### 5. 创建登录页面（可选）

如果你需要自定义登录页面，可以创建一个简单的HTML模板：

```html
<!DOCTYPE html>
<html xmlns:th="http://www.thymeleaf.org">
<head>
    <title>登录页面</title>
</head>
<body>
    <h1>欢迎使用OAuth2.0登录</h1>
    <a href="/oauth2/authorization/github">使用GitHub登录</a>  <!-- 触发OAuth2认证流程 -->
</body>
</html>
```

### 6. 运行应用

启动Spring Boot应用，访问 `http://localhost:8080`，你将看到登录页面。点击登录按钮后，应用会重定向到GitHub（或其他配置的认证提供商）进行认证。认证成功后，用户将被重定向回应用的 `/home`路径。

### 7. 其他配置选项

如果你需要获取更多用户信息，可以创建一个自定义的OAuth2用户服务：

```java
import org.springframework.security.oauth2.client.userinfo.DefaultOAuth2UserService;
import org.springframework.security.oauth2.client.userinfo.OAuth2UserRequest;
import org.springframework.security.oauth2.core.OAuth2AuthenticationException;
import org.springframework.security.oauth2.core.user.OAuth2User;
import org.springframework.stereotype.Service;

@Service
public class CustomOAuth2UserService extends DefaultOAuth2UserService {

    @Override
    public OAuth2User loadUser(OAuth2UserRequest userRequest) throws OAuth2AuthenticationException {
        OAuth2User user = super.loadUser(userRequest);
      
        // 可以在这里处理用户信息，如保存到数据库等
        System.out.println("用户信息: " + user.getAttributes());
      
        return user;
    }
}
```

然后在安全配置中注册这个服务：

```java
@Configuration
public class SecurityConfig {

    @Autowired
    private CustomOAuth2UserService customOAuth2UserService;

    @Bean
    public SecurityFilterChain securityFilterChain(HttpSecurity http) throws Exception {
        http
            .authorizeRequests()
                .antMatchers("/", "/login").permitAll()
                .anyRequest().authenticated()
                .and()
            .oauth2Login()
                .userInfoEndpoint()
                    .userService(customOAuth2UserService);  // 注册自定义用户服务
              
        return http.build();
    }
}
```

### 总结

通过以上步骤，你可以在Spring Boot应用中成功集成OAuth2.0认证。主要包括添加依赖、配置OAuth2客户端、配置Spring Security、创建控制器处理请求等步骤。根据实际需求，你可以进一步扩展功能，如保存用户信息、自定义登录页面等。
